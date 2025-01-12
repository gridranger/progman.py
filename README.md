# progman.py - A Program Manager reimplementation in Python

Launcher inspired by progman.exe from Win 3.1.

It is designed to be platform-independent but platform-dependent development happen currently on the Windows-side first.

It is written in Python v3.13 using TkInter to be as lightweight as possible.

![screenshot.png](docs%2Fscreenshot.png)

## Features already available

* Organizes the app launcher icons to groups displayed in separate windows.
* Group windows can be opened and closed on convinience. Their content and size and position are preserved.
* Groups are prepopulated from the OS' own app launcher to save time on icon creation based on rules.
* App icons can be present in multiple group at the same time.

## Features on the roadmap

* Changing group membership of icons received from the OS.
* Custom icon creation.
* Custom group creation.
* Tile windows and cascade windows feature.

## Long term goals include also...

* Support for document and link icons.
* Support for hybrid groups showing your project's files and you apps using in the project so you can open up a full workspace on a single click.
* Linux support.
