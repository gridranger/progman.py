from tkinter import Tk, Label

from language import Language
from mainwindow import MainWindow
from theme import Theme


class ProgramManager:

    def __init__(self):
        self._root = MainWindow(Language(), Theme())

    def run(self):
        self._root.render()
        self._root.mainloop()


if __name__ == "__main__":
    p = ProgramManager()
    p.run()
