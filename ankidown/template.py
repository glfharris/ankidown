import aqt
from aqt.utils import *
from aqt.qt import *

from .utils import getConfig, writeConfig, sanitize

class TemplaterWidget:
    def __init__(self, mw, widget, parentWindow):
        self.mw = mw
        self.widget = widget
        self.parentWindow = parentWindow

        self.setupOuter()
        self.setupButtonArea()
        self.setupButtons()
        self.setupTemplateText()
        self.setupTemplate()

    def setupOuter(self):
        l = QVBoxLayout()
        self.widget.setLayout(l)
        self.outerLayout = l

    def setupButtonArea(self):
        w = QWidget()
        self.buttonArea = w
        self.buttonArea.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy(7),
            QSizePolicy.Policy(0)))
        self.outerLayout.addWidget(w, 1)

        l = QHBoxLayout()
        self.buttonArea.setLayout(l)
        self.buttonBox = l
        self.buttonBox.setContentsMargins(0,0,0,0)
        self.buttonBox.setSpacing(8)


    def setupButtons(self):
        self.selectTemplate = QPushButton("Select Template", clicked=self.onTemplateSelect)
        self.saveTemplateButton = QPushButton("Save", clicked=self.onTemplateSave)

        self.buttonBox.addWidget(self.selectTemplate, 1)
        self.buttonBox.addWidget(self.saveTemplateButton, 0)

    def setupTemplate(self):
        config = getConfig()

        if config['last_template'] in config['templates'].keys():
            template = Template(name=config['last_template'])
        else:
            name = getOnlyText("New Template name:")
            template = Template(name=name)

        self.setTemplate(template)


    def onTemplateSave(self):
        self.template.save()
        self.setTemplate(self.template)

    def setupTemplateText(self):
        self.templateText = QPlainTextEdit()
        self.templateText.textChanged.connect(self.onTextChanged)
        self.outerLayout.addWidget(self.templateText, 1)

    def onTextChanged(self):
        self.template.text = self.templateText.toPlainText()

    def onTemplateSelect(self):
        config = getConfig()
        template_list = ['Create new Template...'] + list(config['templates'].keys())
        selection = chooseList("Select a Template:", template_list)

        if selection is 0:
            name = getOnlyText("New Template name:")
        else:
            name = template_list[selection]
        template = Template(name=name)
        self.setTemplate(template)

    def setTemplate(self, template):
        config = getConfig()
        self.template = template
        self.templateText.setPlainText(self.template.text)
        self.selectTemplate.setText("Template: {}".format(self.template.name))

        config['last_template'] = self.template.name
        writeConfig(config)
        self.parentWindow.template = self.template

class Template:
    def __init__(self, name='', text='', create=False):
        config = getConfig()
        if name in config['templates'].keys():
            self.load(name)
        else:
            self.name = name
            self.text = text
            self.save()

    def load(self, name):
        config = getConfig()

        if name in config['templates'].keys():
            self.name = name
            self.text = config['templates'][name]['text']
        else:
            showInfo("Template '{}' does not exist".format(name))

    def save(self):
        config = getConfig()

        if not self.name: # TODO handle bad name input
            self.name = getOnlyText("New Template name:")

        if self.name not in config['templates'].keys():
            config['templates'][self.name] = {'text': ''}

        config['templates'][self.name]['text'] = self.text
        writeConfig(config)

    def keys(self):
        # Matches on everything contained within {}
        ret = re.findall("\{[^\{\}]*\}", self.text)
        # Removes all { and } characters from string x
        return [ re.sub("[\{\}]", "", x) for x in ret ]
    
    def gen(self):
        return sanitize(" -", self.text)


