from tkinter import Tk

from progman.assets import asset_storage
from progman.core import State

from .menubar import Menubar
from .progmanwidget import ProgmanWidget


class MainWindow(Tk, ProgmanWidget):

    def __init__(self, state: State) -> None:
        Tk.__init__(self)
        self._state = state
        ProgmanWidget.__init__(self, "root")
        self._icon = None

    @property
    def state(self) -> State:
        return self._state

    def render(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)
        self.geometry("640x480")
        self._icon = asset_storage["progman"]
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
