from tkinter import Event, Tk

from progman.assets import asset_storage
from progman.core import State

from .icondrawer import IconDrawer
from .menubar import Menubar
from .progmanwidgets import ProgmanWidget


class MainWindow(Tk, ProgmanWidget):

    def __init__(self, state: State) -> None:
        Tk.__init__(self)
        self._state = state
        ProgmanWidget.__init__(self, "root")
        self._icon = None
        self._menubar = None
        self._icon_drawer = None

    @property
    def state(self) -> State:
        return self._state

    def render(self) -> None:
        self._render_title()
        self.geometry("640x480")
        self._render_icon()
        self._render_menubar()
        self._render_drawer()
        self.bind("<Configure>", self._update_size)
        self.update_language()
        self.update_theme()
        ProgmanWidget.render(self)

    def _render_title(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)

    def _render_icon(self) -> None:
        self._icon = asset_storage["progman"]
        self.iconphoto(False, self._icon)

    def _render_menubar(self) -> None:
        self._menubar = Menubar(self)
        self.configure(menu=self._menubar)

    def _render_drawer(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._icon_drawer = IconDrawer(self)

    def _set_title(self, *_args: any) -> None:
        self.title(self.get_label("title"))

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)

    def update_theme(self) -> None:
        ProgmanWidget.update_theme(self)
        self.configure(bg=self.theme.background)

    def _update_size(self, event: Event) -> None:
        self._icon_drawer.update_size(event.width, event.height)
