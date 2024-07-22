import google.generativeai as genai
import os
from PIL import Image
import pdf2image
import asyncio

async def gen_notes(
    model: genai.GenerativeModel, 
    prompt: str, 
    pdf_path: str, 
    cutoff: int = None
)-> list[str]:
    imgs = pdf2image.convert_from_path(pdf_path)
    futures = []
    for i, img in enumerate(imgs):
        f = asyncio.to_thread(model.generate_content, [prompt, img])
        futures.append(f)
        if cutoff is not None and i >= cutoff:
            break
    return await asyncio.gather(*futures)