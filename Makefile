
.PHONY: build ui

build: clean ui
	mkdir build/dist
	cp ankidown/* build/dist/
	zip -r -j ./build/ankidown-anki_v21.zip ankidown

clean:
	rm -rf ./build/*

ui: ui/exporter.ui ui/importer.ui
	rm ankidown/ui_*.py
	pyuic5 ui/exporter.ui -o ankidown/ui_exporter.py
	pyuic5 ui/importer.ui -o ankidown/ui_importer.py