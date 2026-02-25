from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text
import gzip
import re
from pathlib import Path




def extract_text(bytes):
    encoding = detect_encoding(bytes)
    try:
        html = bytes.decode(encoding, errors="replace")
    except:
        html = bytes.decode("utf-8", errors="replace")

    text = extract_plain_text(html)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = text.strip()
    return text



if __name__ == "__main__":

    p = Path("data") / "CC" / "example.warc.gz"

    with gzip.open(p, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type != WarcRecordType.response:
                continue
            html_bytes = record.reader.read()
            print(extract_text(html_bytes))
            break

