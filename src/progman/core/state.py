from typing import TYPE_CHECKING

from core.group import Group
from core.language import Language
from core.tags import Tags
from core.theme import Theme

if TYPE_CHECKING:
    from .shortcut import Shortcut


class State:

    def __init__(self) -> None:
        self.language: Language = Language()
        self.theme: Theme = Theme()
        self.shortcuts: list[Shortcut] = []
        self._groups: dict[str, Group] = {}
        self.group_windows = {}
        self.main_window_geometry = ""

    @property
    def groups(self) -> dict[str, Group]:
        if not self._groups:
            for shortcut in self.shortcuts:
                for tag in shortcut.tags:
                    self._groups.setdefault(tag, Group(tag)).append(shortcut)
            self._groups.setdefault(Tags.NEW.value, Group(Tags.NEW.value))
            self._groups.setdefault(Tags.HIDDEN.value, Group(Tags.HIDDEN.value))
        return self._groups

    def add_group(self, group: Group) -> None:
        geometry = f"{group.size[0]}x{group.size[1]}+{group.position[0]}+{group.position[1]}"
        self._groups[group.name] = Group(group.name, group.is_collapsed, geometry)
