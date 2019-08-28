# Ankidown

Ankidown is an in-progress add-on for Anki, the spaced repetition system.
It's primary purpose is to prevent duplicate effort and streamline the creation of Anki cards from your pre-existing non-anki notes.

Currently Ankidown allows you to import a file and it's template, and convert it directly into a pre-existing Note Type (read the Anki manual if this is unfamiliar).

![](https://raw.githubusercontent.com/glfharris/ankidown/master/assets/example.gif)

## Installation

Ankidown is now available on [Ankiweb](https://ankiweb.net/shared/info/38786043), or just using the code `38786043` from within Anki itself.

## Usage

1. Choose/write the template for your notes. Instead of the double curly braces `{{}}`, Ankidown uses the single braces to denote field names such as `{Front}`. Tags can be included using the reserved field name `{Tags}`.
2. Load the files containing your notes. These files can contain multiple notes if you have set the option to do so (see the config).
3. Render. When you load a file, Ankidown will attempt to render the notes using the existing settings. If this is correct you can simply click add or press `Ctrl+Enter`, otherwise make your changes and click preview to view them. Ankidown will do nothing to your collection until your click add, and it will only add whats in the normal note editor on the right.


## Contributing

Everyone is welcome to open issues and to suggest new features. Slight word of warning is that Ankidown is still in the rapid prototyping (read: chaotic) phase, so pull requests might not be the best idea till it's a little more stable.
