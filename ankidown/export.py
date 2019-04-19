from aqt import mw


def noteExport(note, template, destination):
    note_dict = dict(note.items())
    print(note_dict)
    with open(template, "r") as f:
        template = f.read()
    with open("/home/glfharris/first.md", "w+") as g:
        g.write(template.format(**note_dict))
