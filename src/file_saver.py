import os
import hashlib
import time
from pathlib import Path

def get_unique_name(content: str) -> str:
    ts = int(time.time())
    h = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
    return f"generated_content_{ts}_{h}"

def save_html(html: str, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fname = get_unique_name(html) + ".html"
    fpath = os.path.join(output_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    return fpath

def save_image(image_bytes: bytes, output_dir: str, base_name: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fname = base_name + ".png"
    fpath = os.path.join(output_dir, fname)
    with open(fpath, 'wb') as f:
        f.write(image_bytes)
    return fpath
