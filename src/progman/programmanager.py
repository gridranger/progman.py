from core import Recognizer
from platforms import DataHandler, ShortcutCollector
from ui.mainwindow import MainWindow


class ProgramManager:

    def __init__(self) -> None:
        self._data_handler = DataHandler()
        self.app_state = self._data_handler.load()
        self._root = MainWindow(self.app_state)
        self._root.save = self.save

    def run(self) -> None:
        self._load_os_content()
        self._root.render()
        self._root.protocol("WM_DELETE_WINDOW", self.save_on_quit)
        self._root.mainloop()

    def _load_os_content(self) -> None:
        shortcut_set = set(self.app_state.shortcuts)
        shortcut_set.update(ShortcutCollector().collect_links())
        self.app_state.shortcuts = list(shortcut_set)
        for shortcut in self.app_state.shortcuts:
            Recognizer.categorize(shortcut)

    def save(self) -> None:
        self._data_handler.save()

    def save_on_quit(self) -> None:
        self.save()
        self._root.destroy()


if __name__ == "__main__":  # pragma: no cover
    p = ProgramManager()
    p.run()
