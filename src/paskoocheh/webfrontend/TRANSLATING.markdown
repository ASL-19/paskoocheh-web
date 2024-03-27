# Paskoocheh webfrontend translation guide

The new web translations use a file format called [gettext](https://en.wikipedia.org/wiki/Gettext). It’s a standard that’s compatible with a bunch of different translation systems including [Transifex](https://www.transifex.com), but we’re not using it yet. In the meantime you can use [Poedit](https://poedit.net), which should at least be easier to to work with than methods used for past projects. It may have problems with mixed LTR and RTL translations – please let us know if you run into problems.

## Setup

Before you start using [Poedit](https://poedit.net), change the following preferences:

1. Open Poedit -> Preferences, switch to the “General” tab, and make sure “Automatically compile MO file when saving” is disabled:

    ![Poedit general preferences screenshot](TRANSLATING/poedit-preferences-general.png)

2. Open Poedit -> Preferences, switch to the “Advanced” tab, and make sure that the settings look like this:

    ![Poedit advanced preferences screenshot](TRANSLATING/poedit-preferences-advanced.png)

3. In the View menu, make sure that “Sort by Source” and “Group by Context” are checked:

    ![Poedit advanced preferences screenshot](TRANSLATING/poedit-view-menu.png)

## Translating

The translation file is called `django.po`. You may also see a `django.mo` in some places, which you can ignore (it’s a more optimized version of the `.po` file, and only used in code).

To translate a string, enter the translation in the “Translation” box below the “Source text” box. Make sure to save the file when you’re done.

### Contexts

You’ll notice that most listed translations all have a blue box. This is the “context”, and is used to organize the file to some degree, as well as to allow for multiple source strings with the same text (i.e. strings that might be the same in English, but have somewhat different meanings that might translate into different terms).

Translations without a context are used in a variety of places on the site. For these, make sure to read the translation notes.

### Notes

When you select some translations, you’ll see a “Notes for translators” section on the right side of the screen. These notes are written by the developers to (hopefully) help contextualize how and where the string is used.

### Variables

Some translations will contain variables that are substituted with content by the server. You’ll see two different formats, which Poedit will mark above the translation box:

#### Python format

All instances of `%(variable_name)s` (including the “s”) will be replaced. e.g. `All `%(tool_name)s` FAQs` could produce “All Psiphon FAQs”.

#### Python brace format

All instances of `{variable_name}` will be replaced. e.g. “FAQs for `{tool_name}`” could produce “FAQs for Psiphon”.

### “Needs work” toggle

This toggle may be set if the development team changes a source string, and indicates that you might want to double-check that the translation is still valid. You can also use it yourself if you’re unsure of a translation.

### Plurals

A few translations have singular and plural variants. For these, you’ll see separate “Singular” and “Plural” tabs:

![Poedit plural translation screenshots](TRANSLATING/poedit-plural-translation.png)
