from abc import ABC, abstractmethod
from tkinter import Misc

from ui.icon import Icon
from ui.progmanwidgets import ProgmanWidget
from ui.scrollframe import ScrollFrame


class IconDrawer(ABC, ScrollFrame, ProgmanWidget):

    def __init__(self, parent: Misc | None, *args: any, **kwargs: any) -> None:
        ScrollFrame.__init__(self, parent, *args, **kwargs)
        ProgmanWidget.__init__(self, "icon_drawer")
        self._icons: list[Icon] = []
        self._default_geometry = True
        self.viewPort.on_enter = self.on_enter
        self.viewPort.on_leave = self.on_leave

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def render(self) -> None:
        self._render_icons()
        self.grid(row=0, column=0, sticky="nesw")
        ProgmanWidget.render(self)
        self.update_theme()
        self._arrange_icons()

    @abstractmethod
    def _render_icons(self) -> None:
        """Overwrite this."""
        raise NotImplementedError("Implement this to make this work.")

    def _arrange_icons(self) -> None:
        max_columns = self._get_columns()
        for index, icon in enumerate(self._icons):
            row = index // max_columns
            column = index % max_columns
            icon.grid(row=row, column=column)

    def _get_columns(self) -> int:
        if not self._default_geometry:
            return (self.winfo_width() // Icon.WIDTH) or 1
        icon_count = len(self._icons)
        if icon_count < 7:
            return 3
        if icon_count < 9:
            return 4
        if icon_count < 16:
            return 5
        if icon_count < 19:
            return 6
        return 7

    def _get_max_rows(self) -> int:
        if len(self._icons) < 11:
            return 2
        return 3

    def set_initial_geometry(self) -> None:
        if self.master.group_name in self.app_state.suspended_group_windows:
            self._default_geometry = False
            geometry = self.app_state.suspended_group_windows.pop(self.master.group_name)
            self.master.geometry(geometry)
        else:
            self.set_default_geometry()

    def set_default_geometry(self) -> None:
        self.master.geometry(f"{self._get_columns() * (Icon.WIDTH + 6)}x{self._get_max_rows() * Icon.HEIGHT + 20}")

    def update_configuration(self, width: int, height: int) -> None:
        current_config = self.winfo_width(), self.winfo_height()
        if current_config == (width, height):
            return
        self._default_geometry = False
        self.configure(width=width, height=height)
        self.viewPort.configure(width=width, height=height)
        self._arrange_icons()
        self._update_scrollbar()

    def _update_scrollbar(self) -> None:
        last_icon = list(self.viewPort.children.values())[-1] if self.viewPort.children else None
        if last_icon and last_icon.winfo_y() + Icon.HEIGHT > self.winfo_height():
            self._place_scrollbar()
        else:
            self.vsb.grid_forget()
