from fastwarc.warc import ArchiveIterator, WarcRecordType
import gzip
import random
from pathlib import Path
from typing import BinaryIO, cast

from cs336_data.utils import decode_text, extract_text


def sample_warc(path, k):
    skipped = 0
    chosen = None
    chosen_record_id = None

    with gzip.open(path, "rb") as f:
        for record in ArchiveIterator(cast(BinaryIO, f)):
            if record.record_type != WarcRecordType.response:
                continue
            html_bytes = record.reader.read()
            if skipped < k:
                skipped += 1
                continue
            chosen = html_bytes
            chosen_record_id = record.headers.get("WARC-Record-ID")
            break

    if chosen is None:
        raise RuntimeError(f"Not enough response records in {path} to skip {k}")

    return chosen, chosen_record_id


def sample_wet(path, record_id):
    chosen_wet = None

    with gzip.open(path, "rb") as f:
        for record in ArchiveIterator(cast(BinaryIO, f)):
            if record.record_type != WarcRecordType.conversion:
                continue
            wet_bytes = record.reader.read()
            refers_to = record.headers.get("WARC-Refers-To") or record.headers.get(
                "WARC-Refers-To-Record-ID"
            )
            wet_record_id = record.headers.get("WARC-Record-ID")
            if refers_to == record_id or wet_record_id == record_id:
                chosen_wet = wet_bytes
                break

    if chosen_wet is None:
        raise RuntimeError(f"No matching conversion record in {path} for {record_id}")

    return chosen_wet


def main():
    p = Path("data") / "CC" / "example.warc.gz"
    p_wet = Path("data") / "CC" / "example.warc.wet.gz"

    rng = random.Random()
    k = rng.randrange(1, 1001)

    chosen, chosen_record_id = sample_warc(p, k)

    print("\n" + "=" * 72)
    print(f"WARC extracted text (response #{k + 1})")
    print("=" * 72)
    print(extract_text(chosen))

    chosen_wet = sample_wet(p_wet, chosen_record_id)

    print("\n" + "=" * 72)
    print("WET raw text (matched by WARC-Record-ID)")
    print("=" * 72)
    print(decode_text(chosen_wet))


if __name__ == "__main__":
    #main()

    chosen_wet = sample_wet(Path("data") / "CC" / "example.warc.wet.gz", "<urn:uuid:ddbaca76-fb41-4455-a447-bf2ab495c771>")
    print(decode_text(chosen_wet))