from aqt import mw


def modelNames():
    collection = mw.col

    return collection.models.allNames()


def modelFieldNames(model_name):
    collection = mw.col

    model = collection.models.byName(model_name)

    return [field['name'] for field in model['flds']]
