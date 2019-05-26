import aqt
from aqt import mw
from aqt.qt import *

from .notes import noteFormat
from .ui_dialog import Ui_AnkidownDialog

class AnkidownDialog(QDialog, Ui_AnkidownDialog):
    def __init__(self, mw):
        super().__init__()
        self.setupUi(self)

        self.NoteSearchButton.clicked.connect(self.on_search)
        self.NoteList.itemClicked.connect(self.on_click)

        self.show()
        self.activateWindow()
    
    def on_search(self):
        self.NoteList.clear()

        query = self.NoteSearchText.text()
        note_list = mw.col.findNotes(query)
        for note in note_list:
            self.NoteList.addItem(str(note))
    
    def on_click(self, item):
        self.NotePreview.setPlainText(noteFormat(mw.col.getNote(item.text())))
    
    def reject(self):
        aqt.dialogs.markClosed("Ankidown")
        QDialog.reject(self)
    
    def closeWithCallback(self, callback):
        self.reject()
        callback()