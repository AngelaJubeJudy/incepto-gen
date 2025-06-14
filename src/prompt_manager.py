import os
import json
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np

class PromptManager:
    def __init__(self, prompt_dir: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.prompt_dir = prompt_dir
        self.model = SentenceTransformer(embedding_model)
        self.prompts = []
        self.embeddings = None
        self.load_prompts()

    def load_prompts(self):
        self.prompts = []
        for fname in os.listdir(self.prompt_dir):
            if fname.endswith('.json'):
                with open(os.path.join(self.prompt_dir, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.prompts.extend(data)
        self.embeddings = self.model.encode([p['text'] for p in self.prompts])

    def get_prompt_by_id(self, pid: str) -> Dict[str, Any]:
        for p in self.prompts:
            if p['id'] == pid:
                return p
        return {}

    def search(self, input_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        sims = np.dot(self.embeddings, input_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(input_embedding) + 1e-8)
        idxs = np.argsort(sims)[::-1][:top_k]
        return [self.prompts[i] for i in idxs]
