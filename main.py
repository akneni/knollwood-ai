from apikeys import GEMINI_KEY
import google.generativeai as genai
import os
import utils.pdf
import shelve


if not os.path.exists('outputs'):
    os.mkdir('outputs')
if not os.path.exists('dataroom'):
    os.mkdir('dataroom')


tmpl = utils.templates.Templates('./templates/agent-templates.json', './templates/task-templates.json')
dr = utils.dataroom.DataRoom('./dataroom')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction=tmpl.researcher
)
dr.gen_all_notes(model)
print('finished generating all notes')

model = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction=tmpl.writer
)

if not os.path.exists('./outputs/shelve-db'):
    os.makedirs('./outputs/shelve-db')
with shelve.open('./outputs/shelve-db/db') as db:
    for t in tmpl.task_json:
        section = t['section']
        try:
            addition = model.generate_content(f"{tmpl.section_tpl[section]}\n\nUse the following notes to fill out this section:\n{dr.get_notes()}\n\nWRITE EVERYTHING IN PLAIN TEXT, NOT MARKDOWN").text
            print(f"Section: {section}\n{addition}"[:100] + '...\n\n')
        except AttributeError:
            addition = ''
        db[section] = addition
    
utils.build_word_doc('./outputs/shelve-db/db')