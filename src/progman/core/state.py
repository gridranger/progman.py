from typing import TYPE_CHECKING

from .group import Group
from .language import Language
from .tags import Tags
from .theme import Theme

if TYPE_CHECKING:
    from .shortcut import Shortcut


class State:

    def __init__(self) -> None:
        self.language: Language = Language()
        self.theme: Theme = Theme()
        self.shortcuts: list[Shortcut] = []
        self._groups: dict[str, Group] = {
            Tags.HIDDEN.value: Group("hidden"),
            Tags.NEW.value: Group("new")
        }

    @property
    def groups(self) -> dict[str, Group]:
        if not self._groups:
            for shortcut in self.shortcuts:
                for tag in shortcut.tags:
                    self._groups.setdefault(tag, Group(tag)).append(shortcut)
        return self._groups
