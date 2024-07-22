from apikeys import GEMINI_KEY
import google.generativeai as genai
import os
from PIL import Image
import asyncio
import utils.pdf
import shelve

async def get_async():
    response = [asyncio.to_thread(model.generate_content, ["Describe what you see in this image: ", Image.open('data/img.png')]) for _ in range (10)]
    response = await asyncio.gather(*response)
    return [t.text[:10] + '...' for t in response]

def get_sync():
    return [
        model.generate_content(["Describe what you see in this image: ", Image.open('data/img.png')])
        for _ in range (10)
    ]


genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction='You are a VC Analyst. Your job is to read data about VC Funds and their firms and compile a comprehensive list of notes about them. Note that these notes are meant to provide data to your colleges that\'s relevant to making an investment decision.'
)
dr = utils.dataroom.DataRoom('./dataroom')
tmpl = utils.templates.Templates('./templates/agent-templates.json', './templates/task-templates.json')

dr.gen_all_notes(model)
print('finished generating all notes')

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=tmpl.writer
)

with shelve.open('outputs/db') as db:
    for t in tmpl.task_json:
        section = t['section']
        try:
            addition = model.generate_content(f"{tmpl.writer}\n\nNotes:\n{dr.get_notes()}").text
        except AttributeError:
            addition = ''
        db[section] = addition
    
