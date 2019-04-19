
build:
	zip -r -j ./build/ankidown-anki_v21.zip ankidown

clean:
	rm -rf ./build/*

test: testclean
	cp -r ./ankidown ~/.local/share/Anki2/addons21/ankidown-test
	anki

testclean:
	rm -rf ~/.local/share/Anki2/addons21/ankidown-test
