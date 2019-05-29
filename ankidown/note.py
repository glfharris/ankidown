from difflib import get_close_matches

from anki.notes import Note
from aqt import mw

from markdown import markdown as md

from .template import Template
from .vendor.parse import parse

class AnkidownNote:
    def __init__(self, file="", text="", config={}, template=None, note=None):
        self.config = config
        self.file = file
        self.text = text
        self.template = template
        self.note = note

    def render(self, model=None, tmp_template=None):

        if tmp_template:
            template = tmp_template
        else:
            template = self.template

        if not model:
            model_name = template.findSimilar()[0]['model']
            note = Note(mw.col, model=mw.col.models.byName(model_name))
        else:
            note = Note(mw.col, model=model)

        res = parse(template.gen(), self.text)

        for k, v in res.named.items():
            key = get_close_matches(k, note.keys())[0]
            note[key] = md(v)

        self.note = note
