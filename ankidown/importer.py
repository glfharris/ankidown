from anki.hooks import addHook, remHook
from anki.sound import clearAudioQueue

import aqt
from aqt.addcards import AddCards
from aqt.utils import saveGeom, restoreGeom
from aqt.qt import *

from difflib import get_close_matches
from markdown import markdown as md
from re import sub

from .forms.ui_importer import Ui_AnkidownImportDialog
from .vendor.parse import parse

class AnkidownImporter(AddCards):
    def __init__(self, mw):
        QDialog.__init__(self, None, Qt.Window)
        self.Dialog = self
        mw.setupDialogGC(self)
        self.form = Ui_AnkidownImportDialog()
        self.form.setupUi(self)
        self.mw = mw

        self.setupChoosers()
        self.setupEditor()
        self.setupButtons()

        addHook('currentModelChanged', self.onModelChange)
        addHook('reset', self.onReset)
        
        self.onReset()
        restoreGeom(self, "ankidown")
        self.history = []
        self.show()
        self.activateWindow()

    def setupButtons(self):
        AddCards.setupButtons(self)
        self.form.selectFile.clicked.connect(self.onFilePicked)
        self.form.selectTemplate.clicked.connect(self.onTemplatePicked)
        self.form.previewButton.clicked.connect(self.onPreview)

    def onPreview(self):
        text = self.form.noteTextEdit.toPlainText()
        template = self.form.templateTextEdit.toPlainText()

        def sanitize(black_list, template):
            for char in black_list:
                template = sub(r'\{.+?\}', lambda x:x.group().replace(char, '_'), template)
            return template
        template = sanitize(" -", template)
        res = parse(template, text)

        new_note = self.mw.col.newNote()
        for k,v in res.named.items():
            key = get_close_matches(k, new_note.keys())[0]
            new_note[key] = md(v)
        
        self.editor.setNote(new_note)

    
    def onFilePicked(self):
        file_name = aqt.utils.getFile(self, "Choose File to Import", None, key="")
        with open(file_name, "r") as f:
            self.form.noteTextEdit.setPlainText(f.read())
        self.form.selectFile.setText(file_name)

    def onTemplatePicked(self):
        template_name = aqt.utils.getFile(self, "Select a Template to use", None, key="")
        with open(template_name, "r") as f:
            self.form.templateTextEdit.setPlainText(f.read())
        self.form.selectTemplate.setText(template_name)
    
    def _reject(self):
        remHook('reset', self.onReset)
        remHook('currentModelChanged', self.onModelChange)
        clearAudioQueue()
        self.removeTempNote(self.editor.note)
        self.editor.cleanup()
        self.modelChooser.cleanup()
        self.deckChooser.cleanup()
        self.mw.maybeReset()
        saveGeom(self, "ankidown")
        aqt.dialogs.markClosed("Ankidown-Importer")
        QDialog.reject(self)
