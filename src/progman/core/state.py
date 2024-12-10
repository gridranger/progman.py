from typing import TYPE_CHECKING

from .language import Language
from .tags import Tags
from .theme import Theme

if TYPE_CHECKING:
    from .shortcut import Shortcut


class State:

    def __init__(self) -> None:
        self.groups: set[str] = set([tag.value for tag in Tags])
        self.language: Language = Language()
        self.shortcuts: list[Shortcut] = []
        self.theme: Theme = Theme()
