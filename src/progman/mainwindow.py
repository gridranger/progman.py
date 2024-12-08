from tkinter import Tk

from assets import assets
from language import Language
from progmanwidget import ProgmanWidget
from theme import Theme

from src.progman.menubar import Menubar


class MainWindow(Tk, ProgmanWidget):

    def __init__(self, language: Language, theme: Theme) -> None:
        Tk.__init__(self)
        self._language = language
        self._theme = theme
        ProgmanWidget.__init__(self, "root")

    def render(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)
        self.geometry("640x480")
        self._icon = assets["progman"]
        self.iconphoto(False, self._icon)
        menubar = Menubar(self)
        self.configure(menu=menubar)
        menubar.render()
        self.update_language()
        self.update_theme()

    def _set_title(self, *_args: any) -> None:
        self.title(self.get_label("title"))

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)

    def update_theme(self) -> None:
        ProgmanWidget.update_theme(self)
        self.configure(bg=self.theme.background)
