from tkinter import Menu

from ui.progmanwidgets import ProgmanWidget


class Menubar(Menu, ProgmanWidget):

    def __init__(self, *args: any, **kwargs: any) -> None:
        Menu.__init__(self, *args, **kwargs)
        ProgmanWidget.__init__(self, "menu_bar")
        self._file_menu = Menu(self, tearoff=0)

    def render(self) -> None:
        self._file_menu.add_command(label="Save", command=self.master.save)
        self._file_menu.add_command(label="Exit", command=self.quit)
        self.add_cascade(label=self.get_label("file"), menu=self._file_menu)
        self._texts["file"].trace("w", self._set_file_menu_label)

    def _set_file_menu_label(self, *_args: any) -> None:
        self.entryconfig(0, label=self.get_label("file"))

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)
