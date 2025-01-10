from abc import ABC, abstractmethod
from tkinter import Event, Tk

from assets import asset_storage


class Window(ABC):
    DEFAULT_DIMENSIONS = "253x172"

    def __init__(self, icon_name: str) -> None:
        self._icon_name = icon_name
        self._icon = None
        self._icon_drawer = None

    @property
    def geometry_as_string(self) -> str:
        return self.geometry()

    def render(self: Tk) -> None:
        self._render_window()

    @abstractmethod
    def _render_title(self) -> None:
        pass

    def _render_icon(self) -> None:
        self._icon = asset_storage[self._icon_name]
        self.iconphoto(False, self._icon)

    def _render_window(self) -> None:
        self._render_title()
        self.geometry(self.DEFAULT_DIMENSIONS)
        self._render_icon()
        self.bind("<Configure>", self.update_configuration)

    def update_configuration(self, event: Event) -> None:
        if event.widget == self:
            self._icon_drawer.update_configuration(event.width, event.height)

    def render_drawer(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
