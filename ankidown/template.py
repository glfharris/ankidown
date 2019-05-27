import aqt
from aqt.qt import *

class Templater:
    def __init__(self, mw, widget, parentWindow):
        self.mw = mw
        self.widget = widget
        self.parentWindow = parentWindow

        self.setupOuter()
        self.setupButtons()
        self.setupTemplateText()

    def setupOuter(self):
        l = QVBoxLayout()
        self.widget.setLayout(l)
        self.outerLayout = l

    def setupButtons(self):
        self.selectTemplate = QPushButton("Select Template", clicked=self.onTemplateSelect)
        self.outerLayout.addWidget(self.selectTemplate, 1)

    def setupTemplateText(self):
        self.templateText = QPlainTextEdit()
        self.outerLayout.addWidget(self.templateText, 1)

    def onTemplateSelect(self):
        template_name = aqt.utils.getFile(self.widget, "Select a Template to use", None, key="")
        with open(template_name, "r") as f:
            self.templateText.setPlainText(f.read())
        self.selectTemplate.setText(template_name)
        self.parentWindow.onTemplateChange()
