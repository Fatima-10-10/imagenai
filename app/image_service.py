import os
import io
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_TOKEN,
)

async def generate_image(prompt: str) -> bytes:
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell",
    )
    # image is a PIL Image object — convert to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()