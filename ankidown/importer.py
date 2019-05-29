from anki.hooks import addHook, remHook
from anki.sound import clearAudioQueue

import aqt
from aqt.addcards import AddCards
from aqt.utils import saveGeom, restoreGeom, addCloseShortcut, askUser
from aqt.qt import *

from difflib import get_close_matches
from markdown import markdown as md
from re import sub
from os import path

from .note import AnkidownNote
from .template import TemplaterWidget
from .forms.ui_importer import Ui_AnkidownImportDialog
from .vendor.parse import parse
from .utils import getConfig

class AnkidownImporter(AddCards):
    def __init__(self, mw):
        QDialog.__init__(self, None, Qt.Window)
        self.Dialog = self
        mw.setupDialogGC(self)
        self.form = Ui_AnkidownImportDialog()
        self.form.setupUi(self)
        self.mw = mw

        self.history = []
        self.buffer = [AnkidownNote()]

        self.templateWidget = TemplaterWidget(self.mw,
                self.form.templateTab, self)
        self.setupChoosers()
        self.setupEditor()
        self.setupButtons()

        addHook('currentModelChanged', self.onModelChange)
        addHook('reset', self.onReset)
        
        restoreGeom(self, "ankidown")
        addCloseShortcut(self)

        self.setBuffer(0)

        self.onReset()
        self.show()
        self.activateWindow()

    def addCards(self):
        super().addCards()
        self.nextNote()

    def setupButtons(self):
        super().setupButtons()
        self.closeButton.clicked.connect(self.reject)
        self.form.selectFile.clicked.connect(self.onFilePicked)

        self.form.prevButton.clicked.connect(self.prevNote)
        self.form.prevButton.setShortcut("Left")
        self.form.nextButton.clicked.connect(self.nextNote)
        self.form.nextButton.setShortcut("Right")

        self.form.previewButton.clicked.connect(self.onPreview)
        self.form.previewButton.setShortcut("Space")

        self.form.noteTextEdit.textChanged.connect(self.onNoteTextChanged)

    def currentNote(self):
        return self.buffer[self.bufferIndex]

    def nextNote(self):
        if self.bufferIndex + 1 < len(self.buffer):
            self.setBuffer(self.bufferIndex + 1)
        else:
            self.setBuffer(0)

    def prevNote(self):
        if self.bufferIndex is 0:
            self.setBuffer(len(self.buffer) - 1)
        else:
            self.setBuffer(self.bufferIndex - 1)

    def onNoteTextChanged(self):
        text = self.form.noteTextEdit.toPlainText()
        self.currentNote().text = text

    def onPreview(self):
        if not self.currentNote().template:
            self.currentNote().render(tmp_template=self.template)
        else:
            self.currentNote().render()
        self.editor.setNote(self.currentNote().note)


    def onFilePicked(self):
        config = getConfig()
        self.buffer = []
        file_names = aqt.utils.getFile(self,
                "Select File to Import", None, key="ankidown-files", multi=True)
        # Scope for improved performance by only loading text when needed
        for file_name in file_names:
            with open(file_name, "r") as f:
                text = f.read()
                if config["note_separator"]:
                    text = [tmp.lstrip() for tmp in text.split(config["note_separator"])]
                else:
                    text = [text]
                for raw_note in text:
                    self.buffer.append(AnkidownNote(file=file_name, text=raw_note))
        for note in self.buffer:
            note.render(tmp_template=self.template)
        self.setBuffer(0) # Given root index

    def setBuffer(self, index):
        self.bufferIndex = index

        self.form.noteTextEdit.setPlainText(self.buffer[index].text)
        name = path.split(self.buffer[index].file)[1]
        self.form.selectFile.setText("File: {} Note: {} of {}".format(
            name, index + 1, len(self.buffer)))

        if self.currentNote().note:
            self.editor.setNote(self.currentNote().note)

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

    def ifCanClose(self, onOk):
        def afterSave():
            if askUser(_("Close and lose current input?")):
                onOk()

        self.editor.saveNow(afterSave)
