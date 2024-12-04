from tkinter import Menu

from src.progman.progmanwidget import ProgmanWidget


class Menubar(Menu, ProgmanWidget):

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)
        ProgmanWidget.__init__(self, "menu_bar")
        self._file_menu = Menu(self, tearoff=0)

    def render(self):
        self._file_menu.add_command(label="Exit", command=self.quit)
        self.add_cascade(label=self.get_label("file"), menu=self._file_menu)
        self._texts["file"].trace("w", self._set_file_menu_label)

    def _set_file_menu_label(self, *_args):
        self.entryconfig(0, label=self.get_label("file"))

    def update_theme(self):
        ProgmanWidget.update_theme(self)

    def update_language(self):
        ProgmanWidget.update_language(self)
