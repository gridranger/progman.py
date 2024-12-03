from abc import ABC, abstractmethod
from tkinter import BaseWidget
from typing import Union

from language import Language
from theme import Theme


class ProgmanWidget(ABC):

    def __init__(self):
        self.master: Union[BaseWidget, ProgmanWidget]
        self._language = self.master.language if self.master is not None else None
        self._theme = self.master.theme if self.master is not None else None

    @property
    def language(self) -> Language:
        return self._language

    @language.setter
    def language(self, language: Language):
        self._language = language
        self._update_language()
        for child in self.children:
            child.language = self.language

    @property
    def theme(self) -> Theme:
        return self._theme

    @theme.setter
    def theme(self, theme: Theme):
        self._theme = theme
        self._update_theme()
        for child in self.children:
            child.theme = self._theme

    @abstractmethod
    def _update_language(self):
        pass

    @abstractmethod
    def _update_theme(self):
        pass
