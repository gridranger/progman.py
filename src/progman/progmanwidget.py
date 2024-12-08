from abc import ABC, abstractmethod
from tkinter import BaseWidget, StringVar

from language import Language
from theme import Theme


class ProgmanWidget(ABC):

    def __init__(self, lid: str) -> None:
        self.master: BaseWidget | ProgmanWidget
        self._lid = lid
        self._texts = {}

    @property
    def language(self) -> Language:
        return self._language if self.master is None else self.master.language

    def get_label(self, label: str) -> str:
        if not self._texts:
            self.update_language()
        return self._texts[label].get()

    @property
    def theme(self) -> Theme:
        return self._theme if self.master is None else self.master.theme

    def update_language(self) -> None:
        for key, value in self.language.content[self._lid].items():
            self._texts.setdefault(key, StringVar(self, "")).set(value)

    @abstractmethod
    def update_theme(self) -> None:
        for child in self.children:
            if isinstance(child, ProgmanWidget):
                child.update_theme()

    @abstractmethod
    def render(self) -> None:
        for child in self.children:
            if isinstance(child, ProgmanWidget):
                child.render()
