from .shortcut import Shortcut


class Group:

    def __init__(self, name: str) -> None:
        self.name = name
        self.shortcuts = []
        self.is_collapsed = True

    @property
    def is_empty(self) -> bool:
        return not self.shortcuts

    def append(self, element: Shortcut) -> None:
        self.shortcuts.append(element)
