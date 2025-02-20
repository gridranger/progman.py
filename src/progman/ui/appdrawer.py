from tkinter import Misc

from core import Shortcut, Tags
from ui.appicon import AppIcon
from ui.icondrawer import IconDrawer


class AppDrawer(IconDrawer):

    def __init__(self, parent: Misc | None, category: str, *args: any, **kwargs: any) -> None:
        IconDrawer.__init__(self, parent, *args, **kwargs)
        self._category = category

    def _render_icons(self) -> None:
        for shortcut in self.app_state.shortcuts:
            if self._category in shortcut.tags:
                self._icons.append(AppIcon(shortcut, self, self.viewPort))

    def add_icon(self, shortcut: Shortcut) -> None:
        self._icons.append(AppIcon(shortcut, self, self.viewPort))
        self._icons[-1].render()
        self._arrange_icons()

    def delete_icon(self, icon: AppIcon, shortcut: Shortcut) -> None:
        shortcut.tags.remove(self._category)
        if not shortcut.tags:
            if shortcut.managed_by_user and shortcut.link_path:
                shortcut.tags.append(Tags.HIDDEN.value)
                self.app_state.groups[Tags.HIDDEN.value].append(shortcut)
            elif shortcut.managed_by_user:
                self.app_state.shortcuts.remove(shortcut)
            else:
                shortcut.managed_by_user = True
                shortcut.tags.append(Tags.HIDDEN.value)
                self.app_state.groups[Tags.HIDDEN.value].append(shortcut)
        self._icons.remove(icon)
        icon.destroy()
        self._arrange_icons()
