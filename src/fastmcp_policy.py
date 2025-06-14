import numpy as np
from typing import Dict, Any, List
import random

class FastMCPPolicy:
    def __init__(self, prompt_manager, mc_simulations=20):
        self.prompt_manager = prompt_manager
        self.mc_simulations = mc_simulations

    def reward(self, input_embedding, prompt_embedding):
        # 以语义相似度为主
        sim = np.dot(input_embedding, prompt_embedding) / (
            np.linalg.norm(input_embedding) * np.linalg.norm(prompt_embedding) + 1e-8)
        return sim

    def select_prompt(self, input_embedding) -> Dict[str, Any]:
        best_prompt = None
        best_score = -float('inf')
        for _ in range(self.mc_simulations):
            idx = random.randint(0, len(self.prompt_manager.prompts) - 1)
            prompt = self.prompt_manager.prompts[idx]
            prompt_emb = self.prompt_manager.embeddings[idx]
            score = self.reward(input_embedding, prompt_emb)
            if score > best_score:
                best_score = score
                best_prompt = prompt
        return best_prompt
