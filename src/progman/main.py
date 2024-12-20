from core import Recognizer, State
from platforms import ShortcutCollector
from ui.mainwindow import MainWindow


class ProgramManager:

    def __init__(self) -> None:
        self._is_first_run = True  # TODO: calculate it dynamically
        self.app_state = State()
        self._root = MainWindow(self.app_state)

    def run(self) -> None:
        self._load_content()
        self._root.render()
        self._root.mainloop()

    def _load_content(self) -> None:
        if self._is_first_run:
            self.app_state.shortcuts = ShortcutCollector().collect_links()
            for shortcut in self.app_state.shortcuts:
                Recognizer.categorize(shortcut)
        else:
            self._load_saved_state()
            self._update_state()

    def _load_saved_state(self) -> None:
        pass  # TODO

    def _update_state(self) -> None:
        pass  # TODO

    def _set_state(self) -> None:
        pass  # TODO


if __name__ == "__main__":
    p = ProgramManager()
    p.run()
