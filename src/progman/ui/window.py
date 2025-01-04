from abc import ABC, abstractmethod
from tkinter import Tk, Event

from assets import asset_storage


class Window(ABC):
    DEFAULT_DIMENSIONS = "253x172"

    def __init__(self, icon_name: str) -> None:
        self._icon_name = icon_name
        self._icon = None
        self._icon_drawer = None

    def render(self: Tk) -> None:
        self._render_window()

    @abstractmethod
    def _render_title(self) -> None:
        pass

    def _render_icon(self) -> None:
        self._icon = asset_storage[self._icon_name]
        self.iconphoto(False, self._icon)

    def _render_window(self):
        self._render_title()
        self.geometry(self.DEFAULT_DIMENSIONS)
        self._render_icon()
        self.bind("<Configure>", self._update_configuration)

    def _update_configuration(self, event: Event) -> None:
        self._icon_drawer.update_configuration(event.width, event.height)

    def _render_drawer(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
