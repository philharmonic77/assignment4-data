from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text
import re
from pathlib import Path
import random
import fasttext
from nltk.tokenize import word_tokenize


def extract_text(bytes):
    html = decode_text(bytes)

    text = extract_plain_text(html)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = text.strip()
    return text

def decode_text(bytes):
    encoding = detect_encoding(bytes)
    try:
        return bytes.decode(encoding, errors="replace")
    except:
        return bytes.decode("utf-8", errors="replace")
    
def language_identification(text):
    model_path = str(Path("models") / "lid.176.bin")
    model = fasttext.load_model(model_path)
    text = text.replace("\n", " ")
    lang, prob = model.predict(text)

    if len(lang) > 0:
        return lang[0].replace('__label__', ''), prob[0]
    return "unk", 0

def mask_emails(text):
    pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    return re.subn(pattern, "|||EMAIL_ADDRESS|||", text)

def mask_phone_numbers(text):
    pattern = re.compile(r"(?:\+?\d{1,3}[\s\-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s\-]?\d{3,4}[\s\-]?\d{3,4}")
    return re.subn(pattern, "|||PHONE_NUMBER|||", text)

def mask_ips(text):
    pattern = re.compile(r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)")
    return re.subn(pattern, "|||IP_ADDRESS|||", text)   

def mask_pii(text):
    text, _ = mask_emails(text)
    text, _ = mask_phone_numbers(text)
    text, _ = mask_ips(text)
    return text

def classify_nsfw(text):
    model_path = str(Path("models") / "jigsaw_fasttext_bigrams_nsfw_final.bin")
    model = fasttext.load_model(model_path)
    text = text.replace("\n", " ")
    label, score = model.predict(text)

    if len(label) > 0:
        return label[0].replace('__label__', ''), score[0]
    return "unk", 0

def classify_toxic_speech(text):
    model_path = str(Path("models") / "jigsaw_fasttext_bigrams_hatespeech_final.bin")
    model = fasttext.load_model(model_path)
    text = text.replace("\n", " ")
    label, score = model.predict(text)

    if len(label) > 0:
        return label[0].replace('__label__', ''), score[0]
    return "unk", 0

def classify_harmful_content(text):
    label1, score1 = classify_nsfw(text)
    label2, score2 = classify_toxic_speech(text)
    return dict(nsfw_label=label1, nsfw_score=score1, toxic_label=label2, toxic_score=score2)

def gopher_quality_filters(text):
    words = word_tokenize(text)
    word_count = len(words)
    if word_count < 50 or word_count > 100000:
        return False

    mean_word_len = sum(len(w) for w in words) / word_count
    if mean_word_len < 3 or mean_word_len > 10:
        return False

    lines = text.splitlines()
    ellipsis_lines = sum(1 for line in lines if line.rstrip().endswith("..."))
    if ellipsis_lines / max(1, len(lines)) > 0.30:
        return False

    alpha_words = sum(1 for w in words if any(c.isalpha() for c in w))
    if alpha_words / word_count < 0.80:
        return False

    return True


if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.sample_warc import sample_warc

    WARC_PATH = Path("data") / "CC" / "example.warc.gz"
    k = random.Random().randrange(1, 1001)

    html, text_id = sample_warc(WARC_PATH, k)
    text = extract_text(html)

    # lang, prob = language_identification(text)
    # print(f"lang: {lang}, score: {prob:.6f}")
    # print("="*60, text_id, "="*60)
    # print(text[:5000])

    # clean_text = mask_pii(text)
    # print("="*60, text_id, "="*60)
    # print("="*60, "RAW", "="*60)
    # print(text)
    # print("="*60, "MASKED", "="*60)
    # print(clean_text)

    # result = classify_harmful_content(text)
    # print(f"{result["nsfw_label"]}: {result["nsfw_score"]:.4f}<br>{result["toxic_label"]}: {result["toxic_score"]:.4f}")
    # print("="*60, text_id, "="*60)
    # print(text[:5000])

    print(gopher_quality_filters(text))
    print("="*60, text_id, "="*60)
    print(text[:5000])
