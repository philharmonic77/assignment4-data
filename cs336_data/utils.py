from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text
import re
from pathlib import Path
import random
import fasttext

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

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.sample_warc import sample_warc

    WARC_PATH = Path("data") / "CC" / "example.warc.gz"
    k = random.Random().randrange(1, 1001)

    html, text_id = sample_warc(WARC_PATH, k)
    text = extract_text(html)

    lang, prob = language_identification(text)

    print(f"lang: {lang}, score: {prob:.6f}")
    print("="*72, text_id, "="*72)
    print(text[:5000])
