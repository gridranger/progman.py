
from language import Language
from mainwindow import MainWindow
from theme import Theme


class ProgramManager:

    def __init__(self) -> None:
        self._root = MainWindow(Language(), Theme())

    def run(self) -> None:
        self._root.render()
        self._root.mainloop()


if __name__ == "__main__":
    p = ProgramManager()
    p.run()
