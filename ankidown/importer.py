import aqt
from aqt.utils import showText
from aqt.qt import *

from markdown import markdown as md

from .ui_importer import Ui_AnkidownImportDialog
from .parse import parse

class AnkidownImporter(QDialog, Ui_AnkidownImportDialog):
    def __init__(self, mw):
        super().__init__()
        self.setupUi(self)
        self.mw = mw
        self.deckChooser = aqt.deckchooser.DeckChooser(
            mw, self.deckArea)
        self.modelChooser = aqt.modelchooser.ModelChooser(
            mw, self.modelArea)
        self.editor = aqt.editor.Editor(
            mw, self.fieldsArea, self, True)
        
        note = self.mw.col.newNote()
        self.editor.setNote(note, hide=False)

        self.setupButtons()
    
        self.show()
        self.activateWindow()
    
    def setupButtons(self):
        self.chooseFile.clicked.connect(self.onFilePicked)
        self.previewButton.clicked.connect(self.onPreview)
    
    def onPreview(self):
        text = self.noteTextEdit.toPlainText()
        template = self.templateTextEdit.toPlainText()
        res = parse(template, text)

        new_note = self.mw.col.newNote()
        for k,v in res.named.items():
            new_note[k] = md(v)
        
        self.editor.setNote(new_note)

    
    def onFilePicked(self):
        file_name = aqt.utils.getFile(self, "Choose File to Import", None, key="")
        with open(file_name, "r") as f:
            self.noteTextEdit.setPlainText(f.read())
        self.fileLabel.setText(file_name)
    
    def reject(self):
        aqt.dialogs.markClosed("Ankidown-Importer")
        QDialog.reject(self)
    
    def closeWithCallback(self, callback):
        self.reject()
        callback()