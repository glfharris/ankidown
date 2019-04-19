from aqt import mw


def noteExport(note, template, destination):
    note_dict = dict(note.items())
    print(note_dict)
    with open(template, "r") as f:
        template = f.read()
    with open("/home/glfharris/src/anki/ankidown/examples/tests/Pneumothorax.md", "w+") as g:
        g.write(template.format(**note_dict))
