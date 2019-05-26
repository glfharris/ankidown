ANKIDOWN_DIR = ankidown_test
ANKI_ADDONS_DIR = ~/.local/share/Anki2/addons21
.PHONY: build ui

build: clean ui
	mkdir -p build/${ANKIDOWN_DIR}
	cp -r ankidown/* build/${ANKIDOWN_DIR}/
	cd build/${ANKIDOWN_DIR} && zip -r ../ankidown-anki_v21.zip .

clean:
	rm -rf ./build/*

ui: ui/exporter.ui ui/importer.ui
	mkdir -p build/${ANKIDOWN_DIR}/forms && touch build/${ANKIDOWN_DIR}/forms/__init__.py
	pyuic5 ui/exporter.ui -o build/${ANKIDOWN_DIR}/forms/ui_exporter.py
	pyuic5 ui/importer.ui -o build/${ANKIDOWN_DIR}/forms/ui_importer.py

test: build
	rm -rf ${ANKI_ADDONS_DIR}/${ANKIDOWN_DIR}
	cp -r build/${ANKIDOWN_DIR} ${ANKI_ADDONS_DIR}/.
	anki

docs: Readme.md
	tail -n 2 Readme.md | pandoc -f gfm -o build/ankiweb_ankidown.html
