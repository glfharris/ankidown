from difflib import get_close_matches

from anki.notes import Note
from aqt import mw
from aqt.utils import showInfo

from markdown import markdown as md

from .template import Template
from .utils import getConfig
from .vendor.parse import parse


class AnkidownNote:
    def __init__(self, file="", text="", config={}, template=None, note=None):
        self.config = config
        self.file = file
        self.text = text
        self.template = template
        self.note = note

    def render(self, model=None, tmp_template=None, guess_model=False):
        config = getConfig()

        if not self.text:
            self.note = mw.col.newNote()
            return

        if tmp_template:
            template = tmp_template
        else:
            template = self.template

        if not model and not guess_model:
            note = mw.col.newNote()
        elif not model and guess_model and template.bestModel():
            best_model = mw.col.models.byName(template.bestModel())
            note = Note(mw.col, model=best_model)
        else:
            note = Note(mw.col, model=model)

        try:
            res = parse(template.gen(), self.text)
            parse_keys = res.named.keys()
        except:
            showInfo("Unable to Parse template")
            return

        parse_to_key = {}
        for k in parse_keys:
            parse_to_key[k] = get_close_matches(k, template.keys())[0]

        key_to_fields, _ = template.getSimilarity(note.model()["name"])
        if not key_to_fields:
            showInfo("No mapping to Note has been found")
            return
        for k, v in res.named.items():
            if k == "Tags":
                # Uses the normal way Anki processes tag strings
                tags = mw.col.tags.canonify(mw.col.tags.split(v))
                note.tags += tags
            else:
                key = parse_to_key[k]
                if key in key_to_fields.keys():
                    field = key_to_fields[key]
                    if config["format"] is "markdown":
                        note[field] = md(v)
                    else:
                        note[field] = v

        self.note = note
