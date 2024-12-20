from tkinter import PhotoImage, Misc

from assets import asset_storage
from ui.icon import Icon


class GroupIcon(Icon):

    def __init__(self, parent: Misc | None, group_name: str, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, parent, *args, **kwargs)
        self._group_name = group_name

    @property
    def icon(self) -> PhotoImage:
        return asset_storage["group"]

    @property
    def _label(self) -> str:
        return self._group_name

    def _launch(self) -> None:
        self.master._launch_child_window(self._group_name)
