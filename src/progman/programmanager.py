from core import Recognizer
from platforms import DataHandler, ShortcutCollector
from ui.mainwindow import MainWindow


class ProgramManager:

    def __init__(self) -> None:
        self.app_state = DataHandler().load()
        self._root = MainWindow(self.app_state)

    def run(self) -> None:
        self._load_os_content()
        self._root.render()
        self._root.protocol("WM_DELETE_WINDOW", self._root.save_on_quit)
        self._root.mainloop()

    def _load_os_content(self) -> None:
        shortcut_set = set(self.app_state.shortcuts)
        shortcut_set.update(ShortcutCollector().collect_links())
        self.app_state.shortcuts = list(shortcut_set)
        for shortcut in self.app_state.shortcuts:
            Recognizer.categorize(shortcut)


if __name__ == "__main__":
    p = ProgramManager()
    p.run()
