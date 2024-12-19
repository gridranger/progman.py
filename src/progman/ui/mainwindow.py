from tkinter import Tk

from progman.core import State

from .groupdrawer import GroupDrawer
from .menubar import Menubar
from .progmanwidgets import ProgmanWidget
from .window import Window


class MainWindow(Tk, ProgmanWidget, Window):

    def __init__(self, state: State) -> None:
        Tk.__init__(self)
        self._state = state
        ProgmanWidget.__init__(self, "root")
        Window.__init__(self, "progman")
        self._menubar = None

    @property
    def app_state(self) -> State:
        return self._state

    def render(self) -> None:
        Window.render(self)
        self._render_menubar()
        self._render_drawer()
        self.update_language()
        self.update_theme()
        ProgmanWidget.render(self)

    def _render_title(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)

    def _render_menubar(self) -> None:
        self._menubar = Menubar(self)
        self.configure(menu=self._menubar)

    def _render_drawer(self) -> None:
        Window._render_drawer(self)
        self._icon_drawer = GroupDrawer(self)

    def _set_title(self, *_args: any) -> None:
        self.title(self.get_label("title"))

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)

    def update_theme(self) -> None:
        ProgmanWidget.update_theme(self)
        self.configure(bg=self.theme.background)
