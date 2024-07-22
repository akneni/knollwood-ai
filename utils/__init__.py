from .pdf import *
from .templates import *
from .dataroom import *


def extract_text(res):
    try:
        return str(res.text)
    except Exception:
        return ''