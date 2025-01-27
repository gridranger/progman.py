# progman.py

_Launcher inspired by progman.exe from Win 3.1._

[![QualityGate](https://github.com/gridranger/progman.py/actions/workflows/main.yml/badge.svg)](https://github.com/gridranger/progman.py/actions/workflows/main.yml)

It is designed to be platform-independent but platform-dependent development happen currently on the Windows-side first.

It is written in Python v3.13 using TkInter to be as lightweight as possible.

![screenshot.png](docs%2Fscreenshot.png)

## Features already available

* Organizes the app launcher's (or start menu's) icons to groups displayed in separate windows.
* Group windows can be opened and closed on convenience. Their content and size and position are preserved.
* Groups are prepopulated from the OS' own app launcher to save time on icon creation based on rules.
* App icons can be present in multiple group at the same time.
* Custom icon creation.
* Editing icons.
* Custom group creation.

## Features on the roadmap

* Context sensitive menus (in progress).
* Changing group membership of icons received from the OS.
* Tile windows and cascade windows feature.
* Theming options to use your favourite Win3.1 themes or create your own ones.
* Multilanguage support.

## Long term goals include also...

* Support for document and link icons.
* Support for hybrid groups showing your project's files and you apps using in the project so you can open up a full workspace on a single click.
* Linux support.
