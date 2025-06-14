import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# 默认配置
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = os.getenv('PROMPT_DIR', str(BASE_DIR / 'prompts'))
OUTPUT_DIR = os.getenv('OUTPUT_DIR', str(BASE_DIR / 'output'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
WAIT_TIME = int(os.getenv('WAIT_TIME', 3))
MC_SIMULATIONS = int(os.getenv('MC_SIMULATIONS', 20))

# 其他可扩展配置
