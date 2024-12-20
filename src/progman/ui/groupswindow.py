from tkinter import Misc, Toplevel

from ui.window import Window
from ui.appdrawer import AppDrawer
from ui.progmanwidgets import ProgmanWidget


class GroupsWindow(Toplevel, ProgmanWidget, Window):

    def __init__(self, parent: Misc | None, group_name: str, *args: any, **kwargs: any) -> None:
        Toplevel.__init__(self, parent, *args, **kwargs)
        ProgmanWidget.__init__(self, "window")
        Window.__init__(self, "group")
        self._group_name = group_name

    def render(self) -> None:
        Window.render(self)
        self._render_drawer()
        self.update_theme()
        ProgmanWidget.render(self)
        self._icon_drawer.set_initial_geometry()

    def _render_title(self) -> None:
        self.title(self._group_name)

    def _render_drawer(self) -> None:
        Window._render_drawer(self)
        self._icon_drawer = AppDrawer(self, self._group_name)
