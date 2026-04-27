import os
from dotenv import load_dotenv

load_dotenv()

# We use Groq for ultra-low latency inference, critical for market data
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3-32b"