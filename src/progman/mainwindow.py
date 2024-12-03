from tkinter import Tk, Label

from language import Language
from progmanwidget import ProgmanWidget
from theme import Theme


class MainWindow(Tk, ProgmanWidget):

    def __init__(self, language: Language, theme: Theme):
        Tk.__init__(self)
        ProgmanWidget.__init__(self)
        self.language = language
        self.theme = theme

    def render(self):
        label = Label(self, text="Hello, World!", background=self._theme.background)
        label.pack(pady=20)

    def _update_language(self):
        self.title(self.language.title)

    def _update_theme(self):
        self.configure(bg=self.theme.background)
