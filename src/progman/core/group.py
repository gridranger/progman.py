from core.shortcut import Shortcut


class Group:

    def __init__(self, name: str, is_collapsed: bool = True, geometry: str = "") -> None:
        self.name = name
        self.shortcuts = []
        self.is_collapsed = is_collapsed
        self.size = (0, 0)
        self.position = (0, 0)
        if geometry:
            self.set_geometry(geometry)

    @property
    def is_empty(self) -> bool:
        return not self.shortcuts

    def append(self, element: Shortcut) -> None:
        self.shortcuts.append(element)

    def set_geometry(self, geometry: str) -> None:
        size, _delimiter, position = geometry.partition("+")
        width, _delimiter, height = size.partition("x")
        x, _delimiter, y = position.partition("+")
        self.position = (int(x), int(y))
        self.size = (int(width), int(height))
