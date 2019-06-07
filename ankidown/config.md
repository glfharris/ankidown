# Ankidown

Most of Ankidown's config is used internally and requires very minimal input.
If you are making changes here, please make sure they are correctly formatted! Ankidown will not run as expected without this file. Reset to defaults if you're having issues.

### `multiple_notes_per_file`

This setting enables whether Ankidown will try to find multiple notes per file imported. Set to either `true` or `false`.

### `note_separator`

If `multiple_notes_per_file` is set to `true`, Ankidown will use this to split the incoming fields. By default it's `---` which is a linebreak in Markdown.

### `format`

Currently only `markdown` and `raw` are supported. If `markdown` is selected then Ankidown will turn your notes into HTML (the way Anki normally represents its cards).

### `last_template`

Is what it says. Is used to load the last used template on starting Ankidown

### `min_match_ratio`

Ankidown uses a sort of fuzzy match to map template keys to model field names.
This is the minimum ratio of similarity Ankidown will accept in a key:field mapping.
`0.7` seems like an appropriate number, so don't modify unless you're having issues.

### `recent_models`

A list of recently used models inside Ankidown, sorted so the most recent are first. Ankidown uses this to guess what model is most applicable

### `templates`

This is where Ankidown stores all its templates for parsing. You can edit these here if you really want, but there's not much reason to.
