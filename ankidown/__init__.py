from aqt import mw
from aqt.qt import QAction

from .export import noteExport
from .notes import createNote, noteAddOrUpdate
from .models import *


def hello_world():
    note = mw.col.getNote('1550073326829')
    noteExport(
        note, "/home/glfharris/src/anki/ankidown/examples/templates/condition.md", "void")
    print("Hello World, this is Ankidown")


a = QAction("Ankidown", mw)
a.triggered.connect(hello_world)

mw.form.menuTools.addAction(a)
