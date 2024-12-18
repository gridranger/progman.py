from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tkinter import Misc

from .appicon import AppIcon
from .icondrawer import IconDrawer


class AppDrawer(IconDrawer):

    def __init__(self, parent: Misc | None, category: str, *args: any, **kwargs: any) -> None:
        IconDrawer.__init__(self, parent)
        self._category = category

    def _render_icons(self):
        for shortcut in self.state.shortcuts:
            if self._category in shortcut.tags:
                self._icons.append(AppIcon(shortcut, self.viewPort))
