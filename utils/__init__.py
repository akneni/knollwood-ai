from .pdf import *
from .templates import *
from .dataroom import *

from docx import Document
import shelve
import shutil

def extract_text(res):
    try:
        return str(res.text)
    except Exception:
        return ''

def build_word_doc(shelve_db_path, fund_name: str = None):
    with shelve.open(shelve_db_path) as db:
        d = {k:v for k,v in db.items()}
        if fund_name is not None:
            d['[[Fund Name]]'] = fund_name
        
        find_replace_in_document(
            "./templates/TEMPLATE FUND Screening Memo.docx",
            d,
            "./outputs/screening-memo.docx",
        )

def find_replace_in_document(doc_path, replacements, output_path):
    doc = Document(doc_path)
    
    for paragraph in doc.paragraphs:
        for old_text, new_text in replacements.items():
            if old_text in paragraph.text:
                paragraph.text = paragraph.text.replace(old_text, new_text)
        
    doc.save(output_path)
