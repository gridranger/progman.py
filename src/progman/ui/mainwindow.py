from tkinter import Event, Tk

from core import State
from platforms import DataHandler
from ui.groupdrawer import GroupDrawer
from ui.menubar import Menubar
from ui.progmanwidgets import ProgmanWidget
from ui.window import Window


class MainWindow(Tk, ProgmanWidget, Window):

    def __init__(self, state: State) -> None:
        Tk.__init__(self)
        self._state = state
        ProgmanWidget.__init__(self, "root")
        Window.__init__(self, "progman")
        self._menubar = None
        self._data_handler = DataHandler(self.app_state)

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
        self._icon_drawer.set_initial_geometry()
        self.bind("<Map>", self._on_deiconify)
        self.bind("<Unmap>", self._on_iconify)

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
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def save(self) -> None:
        self._data_handler.save()

    def save_on_quit(self) -> None:
        self.save()
        self.destroy()

    def _on_iconify(self, event: Event) -> None:
        if event.widget == self:
            self._icon_drawer.minimize_child_windows()

    def _on_deiconify(self, event: Event) -> None:
        if event.widget == self:
            self._icon_drawer.restore_child_windows()
            self.focus_set()
