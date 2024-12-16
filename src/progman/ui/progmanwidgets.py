from tkinter import BaseWidget, Canvas, Frame, StringVar

from progman.core import Language, State, Theme


class ProgmanWidget:

    def __init__(self, lid: str) -> None:
        self.master: BaseWidget | ProgmanWidget
        self._lid = lid
        self._texts = {}

    @property
    def state(self) -> State:
        return self.master.state

    @property
    def language(self) -> Language:
        return self.state.language

    @property
    def theme(self) -> Theme:
        return self.state.theme

    def get_label(self, label: str) -> str:
        if not self._texts:
            self.update_language()
        return self._texts[label].get()

    def update_language(self) -> None:
        for key, value in self.language.content[self._lid].items():
            self._texts.setdefault(key, StringVar(self, "")).set(value)

    def update_theme(self) -> None:
        for child in self.children:
            if isinstance(child, ProgmanWidget):
                child.update_theme()

    def render(self) -> None:
        for child in self.children.values():
            if isinstance(child, ProgmanWidget):
                child.render()


class ProgmanFrame(Frame, ProgmanWidget):
    pass


class ProgmanCanvas(Canvas, ProgmanWidget):
    pass
