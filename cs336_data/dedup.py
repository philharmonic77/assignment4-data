from typing import List, Sequence
from os import PathLike
from pathlib import Path
import hashlib

def hash_line(line: str) -> bytes:
    return hashlib.md5(line.encode("utf-8")).digest()


def exact_deduplication(
    input_paths: Sequence[PathLike[str] | str],
    output_dir: PathLike[str] | str,
) -> None:

    counter = {}

    # First pass: count line occurrences
    for path in input_paths:
        path = Path(path)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                h = hash_line(line.rstrip("\n"))
                counter[h] = counter.get(h, 0) + 1

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Second pass: write only unique lines
    for path in input_paths:
        path = Path(path)
        output_path = output_dir / path.name

        with open(path, "r", encoding="utf-8", errors="replace") as f_in, \
             open(output_path, "w", encoding="utf-8") as f_out:

            for line in f_in:
                h = hash_line(line.rstrip("\n"))
                if counter[h] == 1:
                    f_out.write(line)
