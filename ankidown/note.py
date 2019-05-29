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

        if not model:
            note = mw.col.newNote()
        else:
            note = Note(mw.col, model=model)

        if tmp_template:
            template = tmp_template.gen()
        else:
            template = self.template.gen()

        res = parse(template, self.text)

        for k, v in res.named.items():
            key = get_close_matches(k, note.keys())[0]
            note[key] = md(v)

        self.note = note
