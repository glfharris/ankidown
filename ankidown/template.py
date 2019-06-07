import aqt
from aqt.utils import *
from aqt.qt import *

from .utils import (
    getConfig,
    writeConfig,
    sanitize,
    similar,
    modelFieldNames,
    modelNames,
)


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
        self.buttonArea.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy(7), QSizePolicy.Policy(0))
        )
        self.outerLayout.addWidget(w, 1)

        l = QHBoxLayout()
        self.buttonArea.setLayout(l)
        self.buttonBox = l
        self.buttonBox.setContentsMargins(0, 0, 0, 0)
        self.buttonBox.setSpacing(8)

    def setupButtons(self):
        self.selectTemplate = QPushButton(
            "Select Template", clicked=self.onTemplateSelect
        )
        self.saveTemplateButton = QPushButton("Save", clicked=self.onTemplateSave)

        self.buttonBox.addWidget(self.selectTemplate, 1)
        self.buttonBox.addWidget(self.saveTemplateButton, 0)

    def setupTemplate(self):
        config = getConfig()

        if config["last_template"] in config["templates"].keys():
            template = Template(name=config["last_template"])
        else:
            name = getOnlyText("New Template name:")
            if not name:
                return
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
        template_list = ["Create new Template..."] + list(config["templates"].keys())
        selection = chooseList("Select a Template:", template_list)

        if selection is 0:
            name = getOnlyText("New Template name:")
            if not name:
                return
        else:
            name = template_list[selection]
        template = Template(name=name)
        self.setTemplate(template)

    def setTemplate(self, template):
        config = getConfig()
        self.template = template
        self.templateText.setPlainText(self.template.text)
        self.selectTemplate.setText("Template: {}".format(self.template.name))

        config["last_template"] = self.template.name
        writeConfig(config)
        self.parentWindow.template = self.template


class Template:
    def __init__(self, name="", text="", create=False):
        config = getConfig()
        if name in config["templates"].keys():
            self.name = name
            self.text = config["templates"][self.name]["text"]
        else:
            self.name = name
            self.text = text
            self.save()

    def save(self):
        config = getConfig()

        if not self.name:  # TODO handle bad name input
            name = getOnlyText("New Template name:")

            if not name:
                return
            else:
                self.name = name

        if self.name not in config["templates"].keys():
            config["templates"][self.name] = {"text": ""}

        config["templates"][self.name]["text"] = self.text
        writeConfig(config)

    def keys(self):
        # Matches on everything contained within {} that isn't a `{` or a `}`
        ret = re.findall("\{[^\{\}]*\}", self.text)
        # Removes all { and } characters from string x
        return [re.sub("[\{\}]", "", x) for x in ret]

    def gen(self):
        return sanitize(" -", self.text)

    def bestModel(self):
        config = getConfig()
        sims = self.findSimilar()
        maximums = []

        maximums.append(sims[0]["model"])
        for mod in sims[1:]:
            if mod["tot"] == sims[0]["tot"]:
                maximums.append(mod["model"])

        if len(maximums) > 1:  # if thers several equal return most recent
            recents = []
            for mod in maximums:
                if mod in config["recent_models"]:
                    recents.append(
                        {"model": mod, "rank": config["recent_models"].index(mod)}
                    )
            recents = sorted(recents, key=lambda x: x["rank"])
            if len(recents) > 0:
                return recents[0]["model"]
            else:
                # If several good matches but none are recent, just guess
                return maximums[0]
        elif len(maximums) == 1:
            return maximums[0]  # If there's only one match just return it
        else:
            return None

    def findSimilar(self):
        model_names = modelNames()
        totals = []
        for mod in model_names:
            _, b = self.getSimilarity(mod)
            totals.append({"model": mod, "tot": sum(b.values())})

        return sorted(totals, key=lambda x: x["tot"], reverse=True)

    def getSimilarity(self, model_name):
        config = getConfig()
        fields = modelFieldNames(model_name)
        ret = []
        max_ratios = {}
        key_field_map = {}

        for key in self.keys():
            for field in fields:
                ret.append({"key": key, "field": field, "ratio": similar(key, field)})
        ret.sort(key=lambda pair: pair["ratio"], reverse=True)

        for pair in ret:
            if pair["key"] not in key_field_map.keys():
                if pair["field"] not in key_field_map.values():
                    if pair["ratio"] >= config["min_match_ratio"]:
                        max_ratios[pair["key"]] = pair["ratio"]
                        key_field_map[pair["key"]] = pair["field"]

        return key_field_map, max_ratios
