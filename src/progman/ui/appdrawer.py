from tkinter import Misc

from ui.appicon import AppIcon
from ui.icondrawer import IconDrawer


class AppDrawer(IconDrawer):

    def __init__(self, parent: Misc | None, category: str, *args: any, **kwargs: any) -> None:
        IconDrawer.__init__(self, parent, *args, **kwargs)
        self._category = category

    def _render_icons(self) -> None:
        for shortcut in self.app_state.shortcuts:
            if self._category in shortcut.tags:
                self._icons.append(AppIcon(shortcut, self.viewPort))

    def _store_configuration(self) -> None:
        self.app_state.groups[self._category].set_geometry(self.master.geometry())
