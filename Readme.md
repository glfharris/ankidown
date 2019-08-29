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

## Rationale

First and foremost, this is a hobby project for me. I made it mostly to help some of the issues I was having with Anki at the time, and to see if I could. If you don't experience the same problems with Anki, this add-on probably won't help you.

### Text Editing

Personally I'm not a great fan of the text editor in Anki. It's ok for the quick session, but if making cards in bulk it gets tiresome, and I'd prefer to use a tool better suited.

### Note Referencing

If I'm spending all this time writing notes, I want to be able to read over them easily, and to have all my notes in one place. This allows me to write notes in the form of structured markdown documents, and have cards generated from them easily.

For instance, when I was trying to learn about medications I had a little fact sheet on each drug, including things like indication, side effects, contraindications, doses, and mechanism, keeping all the information in one place, and then made a note type that would have the requisite cards.

### Curation

I'm not particularly fond of the existing way Anki imports cards as it doesn't give you much of a chance to edit/review before adding them to your collection, and once in the collection they're more difficult to find. I feel this especially when importing other peoples cards, as I often would want to edit them slightly into my words for example.

I think Ankidown helps in two ways, firstly you don't need to share opaque anki export objects, but just text files (for example written with others in google docs), and secondly gives you a chance to edit the cards before commiting them to your collection.

## Contributing

Everyone is welcome to open issues and to suggest new features. Slight word of warning is that Ankidown is still in the rapid prototyping (read: chaotic) phase, so pull requests might not be the best idea till it's a little more stable.
