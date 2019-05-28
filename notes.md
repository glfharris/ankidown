# Things about the Anki code base

* `key` is used all over the place to allow restoring previous settings
* Use `aqt.utils` where possible
* Save and restore Geom allows for remembering windows sizes
* `cb` is used in some functions to allow for callbacks
* The `anki/designer/*.ui` files get placed in `aqt.forms`
* Need to `remHook` on cleanup
* Anki *really* hates trailing commas in `config.json`
