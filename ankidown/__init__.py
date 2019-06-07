import aqt
from aqt import mw, DialogManager, dialogs
from aqt.qt import QAction, QInputDialog, QMenu

from .importer import AnkidownImporter

DialogManager._dialogs["Ankidown-Importer"] = [AnkidownImporter, None]


def open_importer():
    aqt.dialogs.open("Ankidown-Importer", mw)


ankidown_menu = QMenu("Ankidown", mw)

a = ankidown_menu.addAction("Import")
a.triggered.connect(open_importer)

mw.form.menuTools.addMenu(ankidown_menu)
