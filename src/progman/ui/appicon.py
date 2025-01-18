from subprocess import Popen
from tkinter import PhotoImage
from tkinter.constants import DISABLED

from core import Shortcut, MenuItem
from platforms import IconLoader
from ui.icon import Icon


class AppIcon(Icon):

    def __init__(self, shortcut: Shortcut, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, *args, **kwargs)
        self._shortcut = shortcut
        self._menu_items = [
            MenuItem("copy", state=DISABLED),
            MenuItem("copy_to", state=DISABLED),
            MenuItem("move_to", state=DISABLED),
            MenuItem("delete", state=DISABLED),
            MenuItem("properties", state=DISABLED)
        ]

    @property
    def icon(self) -> PhotoImage:
        if self._icon is None:
            self._icon = IconLoader.load(self._shortcut)
        return self._icon

    @property
    def _label(self) -> str:
        if len(self._shortcut.name) > 20:
            return self._shortcut.name[:17] + "..."
        return self._shortcut.name

    def _launch(self) -> None:
        Popen(self._shortcut.launch_command)

    def rename(self, new_name: str) -> None:
        self._shortcut.name = new_name
        self._text_label.configure(text=new_name)
