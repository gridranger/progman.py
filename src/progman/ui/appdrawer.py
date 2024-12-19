from tkinter import Misc

from .appicon import AppIcon
from .icondrawer import IconDrawer


class AppDrawer(IconDrawer):

    def __init__(self, parent: Misc | None, category: str, *args: any, **kwargs: any) -> None:
        IconDrawer.__init__(self, parent, *args, **kwargs)
        self._category = category

    def _render_icons(self) -> None:
        for shortcut in self.app_state.shortcuts:
            if self._category in shortcut.tags:
                self._icons.append(AppIcon(shortcut, self.viewPort))
