from tkinter import PhotoImage

from progman.core import Shortcut

from .icon import Icon
from ..platforms import IconLoader


class GroupIcon(Icon):

    def __init__(self, group_name: str, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, *args, **kwargs)
        self._group_name = group_name
    
    @property
    def icon(self) -> PhotoImage:
        pass

    @property
    def _name(self) -> str:
        return self._group_name
    
    def _launch(self) -> None:
        pass
