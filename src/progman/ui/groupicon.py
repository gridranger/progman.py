from tkinter import PhotoImage

from ..assets import asset_storage
from .icon import Icon


class GroupIcon(Icon):

    def __init__(self, group_name: str, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, *args, **kwargs)
        self._group_name = group_name

    @property
    def icon(self) -> PhotoImage:
        return asset_storage["group"]

    @property
    def _label(self) -> str:
        return self._group_name

    def _launch(self) -> None:
        if self.state.groups[self._group_name].is_collapsed:
            pass
        else:
            pass
