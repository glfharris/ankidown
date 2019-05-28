from aqt import mw

def getConfig():
    return mw.addonManager.getConfig(__name__.split(".")[0])

def writeConfig(config):
    mw.addonManager.writeConfig(__name__.split(".")[0], config)
