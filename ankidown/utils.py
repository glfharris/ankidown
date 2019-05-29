from difflib import SequenceMatcher
from re import sub

from aqt import mw

def getConfig():
    return mw.addonManager.getConfig(__name__.split(".")[0])

def writeConfig(config):
    mw.addonManager.writeConfig(__name__.split(".")[0], config)

def sanitize(black_list, string):
    for char in black_list:
        string = sub(r'\{.+?\}', lambda x:x.group().replace(char, '_'), string)

    return string

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def modelFieldNames(model_name):
    collection = mw.col
    model = collection.models.byName(model_name)
    return [field['name'] for field in model['flds']]

def modelNames():
    collection = mw.col

    return collection.models.allNames()


