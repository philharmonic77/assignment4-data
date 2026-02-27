from typing import Sequence
from os import PathLike
from pathlib import Path
import hashlib
import re
import unicodedata
from itertools import combinations
from collections import defaultdict
import random
import shutil

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


def minhash_deduplication(
    input_paths: Sequence[PathLike[str] | str],
    num_hashes: int,
    num_bands: int,
    ngram_n: int,
    jaccard_threshold: float,
    output_dir: PathLike[str] | str,
) -> None:
    
    paths = list(input_paths)
    
    # generate candidate
    candidate = [dict() for _ in range(num_bands)]
    doc_id = 0
    assert num_hashes % num_bands == 0
    band_length = num_hashes // num_bands
    for path in paths:
        signature = compute_minhash(path, num_hashes, ngram_n)
        for i in range(num_bands):
            band = signature[i * band_length: (i+1) * band_length]
            band = tuple(band)
            if band in candidate[i]:
                candidate[i][band].append(doc_id)
            else:
                candidate[i][band] = [doc_id]
        doc_id += 1

    # generate candidate pair
    candidate_pairs: set[tuple[int, int]] = set()
    for i in range(num_bands):
        for band, doc_ids in candidate[i].items():
            if len(doc_ids) > 1:
                candidate_pairs.update(generate_pairs(doc_ids))

    # compute jaccard, find duplicated pairs, run clustering
    num_docs = len(paths)
    uf = UnionFind(num_docs)
    for doc_id1, doc_id2 in candidate_pairs:
        with open(paths[doc_id1], "r", encoding="utf-8", errors="ignore") as f:
            doc1 = f.read()
        doc1 = normalize_text(doc1)
        ngrams1 = set(generate_word_ngrams(doc1, ngram_n))
        with open(paths[doc_id2], "r", encoding="utf-8", errors="ignore") as f:
            doc2 = f.read()
        doc2 = normalize_text(doc2)
        ngrams2 = set(generate_word_ngrams(doc2, ngram_n))

        score = compute_jaccard(ngrams1, ngrams2)
        if score >= jaccard_threshold:
            uf.union(doc_id1, doc_id2)

    clusters = defaultdict(list)

    for doc_id in range(num_docs):
        root = uf.find(doc_id)
        clusters[root].append(doc_id)

    # randomly remove all but one of the documents in each cluster
    to_remove: set[int] = set()
    for cluster in clusters.values():
        if len(cluster) > 1:
            keep = random.choice(cluster)
            for doc_id in cluster:
                if doc_id != keep:
                    to_remove.add(doc_id)

    # write to the output dir 
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, path in enumerate(paths):
        if i not in to_remove:
            file_name = Path(path).name
            shutil.copy2(path, output_dir / file_name)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        ch for ch in text
        if unicodedata.category(ch) != "Mn"
    )
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def generate_word_ngrams(text: str, n: int):
    tokens = text.split()
    for i in range(len(tokens) - n + 1):
        yield " ".join(tokens[i:i+n])

def compute_minhash(
        path: PathLike[str] | str,
        num_hashes: int,
        ngram_n: int,
) -> list[int]:

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    text = normalize_text(text)

    signature = [2**128 - 1] * num_hashes

    for ngram in generate_word_ngrams(text, ngram_n):
        for i in range(num_hashes):
            
            h = hashlib.md5((str(i) + ngram).encode("utf-8")).hexdigest()
            h_val = int(h, 16)

            if h_val < signature[i]:
                signature[i] = h_val

    return signature

def generate_pairs(doc_ids: list[int]) -> set[tuple[int, int]]:
    return {
        (min(a, b), max(a, b))
        for a, b in combinations(doc_ids, 2)
    }

def compute_jaccard(a: set[str], b:set[str]):
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
    