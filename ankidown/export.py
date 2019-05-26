from aqt import mw


def noteExport(note, template, destination):
    note_dict = dict(note.items())
    with open(template, "r") as f:
        template = f.read()
    with open("C:/Users/glfha/src/anki-tmp/ankidown/examples/tests/Pneumothorax.md", "w", encoding="utf-8") as g:
        
        g.write(template.format(**note_dict))