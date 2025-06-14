import os
import openai
from typing import Dict, Any
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_html(prompt: str, user_input: str) -> str:
    full_prompt = f"{prompt}\n\nUser Input: {user_input}\n\nGenerate a complete HTML page as described above."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional web designer and HTML generator."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        html_code = response['choices'][0]['message']['content']
        return html_code
    except Exception as e:
        print(f"[ERROR] LLM API 调用失败: {e}")
        return ""
