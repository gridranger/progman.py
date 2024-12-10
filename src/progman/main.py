from platforms import ShortcutCollector

from progman.core import Recognizer, State
from progman.ui.mainwindow import MainWindow


class ProgramManager:

    def __init__(self) -> None:
        self._is_first_run = True  # TODO: calculate it dynamically
        self.state = State()
        self._root = MainWindow(self.state)

    def run(self) -> None:
        self._load_content()
        self._root.render()
        self._root.mainloop()

    def _load_content(self) -> None:
        if self._is_first_run:
            self.state.shortcuts = ShortcutCollector().collect_links()
            for shortcut in self.state.shortcuts:
                Recognizer.categorize(shortcut)
                self.state.groups.update(shortcut.tags)
        else:
            self._load_saved_state()
            self._update_state()
        self._set_state()

    def _load_saved_state(self) -> None:
        pass  # TODO

    def _update_state(self) -> None:
        pass  # TODO

    def _set_state(self) -> None:
        pass  # TODO


if __name__ == "__main__":
    p = ProgramManager()
    p.run()
