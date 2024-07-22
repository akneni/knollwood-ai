import os
# import pdf
import asyncio
from PIL import Image
import google.generativeai as genai

class DataRoom:
    VALID_FILES = ['.txt', '.png', '.md', '.pdf']

    def __init__(self, dataroom_path: str) -> None:
        self.dataroom_path = dataroom_path
        self.files = os.listdir(dataroom_path)
        self.filepaths = [
            os.path.join(dataroom_path, p)
            for p in os.listdir(dataroom_path)
        ]

        self.file_notes = {i:'note notes yet' for i in self.files}

        for f in self.files:
            if not any(f.endswith(i) for i in self.VALID_FILES):
                print(f'WARNING: `{f}` is not a supported file format')

    def get_text_notes(self, model: genai.GenerativeModel):
        for file, filepath in zip(self.files, self.filepaths):
            if not any(file.endswith(i) for i in ('.md', '.txt')):
                continue
            with open(filepath, 'r') as f:
                self.file_notes[file] = f.read()
            
    def gen_pdf_notes(self, model: genai.GenerativeModel):
        for file, filepath in zip(self.files, self.filepaths):
            if not file.endswith('.pdf'):
                continue
            f = gen_notes(model, 'Write notes about this slide in markdown.', filepath)
            res = asyncio.run(f)
            notes = ''
            for i in res:
                try:
                    notes += str(i.text) + "\n\n"
                except AttributeError:
                    pass

            self.file_notes[file] = notes

    def gen_img_notes(self, model: genai.GenerativeModel):
        for file, filepath in zip(self.files, self.filepaths):
            if not file.endswith('.png'):
                continue
            notes = model.generate_content(['Write notes about this in markdown.', Image.open(filepath)])
            try:
                self.file_notes[file] = notes.text
            except AttributeError:
                pass    
    def gen_all_notes(self, model: genai.GenerativeModel):
        self.get_text_notes(model)
        self.gen_pdf_notes(model)
        self.gen_img_notes(model)
    
    def get_notes(self) -> str:
        return '\n\n\n'.join(f'Notes for file: `{k}`:\n{v}' for k, v in self.file_notes)
    



## TEMP
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
)-> list:
    imgs = pdf2image.convert_from_path(pdf_path)
    futures = []
    for i, img in enumerate(imgs):
        f = asyncio.to_thread(model.generate_content, [prompt, img])
        futures.append(f)
        if cutoff is not None and i >= cutoff:
            break
    return await asyncio.gather(*futures)