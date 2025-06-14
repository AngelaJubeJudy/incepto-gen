import re
import os
from PIL import Image
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from torchvision import transforms
from typing import Dict, Any

# 加载文本和图片模型
text_model = SentenceTransformer('all-MiniLM-L6-v2')
try:
    import clip
    clip_model, preprocess = clip.load("ViT-B/32", device="cpu")
except ImportError:
    clip_model, preprocess = None, None


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def text_to_embedding(text: str) -> np.ndarray:
    return text_model.encode([clean_text(text)])[0]

def image_to_embedding(image_path: str) -> np.ndarray:
    if clip_model is None:
        raise ImportError("CLIP 未安装，请安装 clip 包")
    image = preprocess(Image.open(image_path)).unsqueeze(0)
    with torch.no_grad():
        embedding = clip_model.encode_image(image)
    return embedding.cpu().numpy()[0]

def process_chat_log(chat_text: str) -> Dict[str, Any]:
    # 去除时间戳、用户名等元数据
    lines = chat_text.splitlines()
    content = [re.sub(r'^\[.*?\]|^\w+:', '', l).strip() for l in lines]
    content = [l for l in content if l]
    merged = ' '.join(content)
    embedding = text_to_embedding(merged)
    return {'cleaned': merged, 'embedding': embedding}

def process_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    if 'text' in input_data:
        result['text_embedding'] = text_to_embedding(input_data['text'])
    if 'image' in input_data:
        result['image_embedding'] = image_to_embedding(input_data['image'])
    if 'chat' in input_data:
        result['chat'] = process_chat_log(input_data['chat'])
    return result
