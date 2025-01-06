from tkinter import Misc, Toplevel, Event

from ui.window import Window
from ui.appdrawer import AppDrawer
from ui.progmanwidgets import ProgmanWidget


class GroupWindow(Toplevel, ProgmanWidget, Window):
    FIELDS_TO_SAVE = ["group_name", "geometry_as_string"]

    def __init__(self, parent: Misc | None, group_name: str, *args: any, **kwargs: any) -> None:
        Toplevel.__init__(self, parent, *args, **kwargs)
        ProgmanWidget.__init__(self, "window")
        Window.__init__(self, "group")
        self._group_name = group_name

    @property
    def group_name(self) -> str:
        return self._group_name

    def render(self) -> None:
        Window.render(self)
        self._render_drawer()
        self.update_theme()
        ProgmanWidget.render(self)
        self._icon_drawer.set_initial_geometry()
        self.bind("<Destroy>", self._on_destroy)

    def _render_title(self) -> None:
        self.title(self._group_name)

    def _render_drawer(self) -> None:
        Window._render_drawer(self)
        self._icon_drawer = AppDrawer(self, self._group_name)

    def _on_destroy(self, event: Event) -> None:
        if event.widget == self:
            self.app_state.group_windows.pop(self._group_name)
            self.app_state.suspended_group_windows[self._group_name] = self.geometry_as_string

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)
