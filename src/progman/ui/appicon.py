from subprocess import Popen
from tkinter import PhotoImage

from progman.core import Shortcut

from .icon import Icon
from ..platforms import IconLoader


class AppIcon(Icon):

    def __init__(self, shortcut: Shortcut, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, *args, **kwargs)
        self._shortcut = shortcut

    @property
    def icon(self) -> PhotoImage:
        if self._icon is None:
            self._icon = IconLoader.load(self._shortcut)
        return self._icon

    @property
    def _name(self) -> str:
        return self._shortcut.name

    def _launch(self) -> None:
        Popen(self._shortcut.launch_command)

    def rename(self, new_name: str) -> None:
        self._shortcut.name = new_name
        self._text_label.configure(text=new_name)
