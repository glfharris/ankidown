from anki.notes import Note
from anki.utils import fieldChecksum
from aqt import mw


def createNote(deck, model_name, fields, tags=[]):
    collection = mw.col
    model = collection.models.byName(model_name)

    note = Note(collection, model)
    note.model()['did'] = deck
    note.tags = tags + ['Testing-Ankidown']

    for k, v in fields.items():
        note[k] = v

    return note


def noteUpdate(note):
    original = _getOriginal(note)

    for name, field in note.items():
        original[name] = field

    original.flush()


def _getOriginal(note):
    csum = fieldChecksum(note.fields[0])
    original_nid = mw.col.db.first("select id from notes where csum == {} and id != {} and mid == {}".format(
        csum, note.id, note.mid))[0]
    return mw.col.getNote(original_nid)


def noteAddOrUpdate(note):
    if note.dupeOrEmpty() is False:
        mw.col.addNote(note)
    elif note.dupeOrEmpty() is 2:
        noteUpdate(note)
