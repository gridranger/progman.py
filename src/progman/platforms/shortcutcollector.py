from abc import ABC, abstractmethod

from progman.shortcut import Shortcut


class ShortcutCollector(ABC):
    tags = ["Accessories", "Games", "Main", "Multimedia", "Office", "Internet", "Creativity"]

    @abstractmethod
    def collect_links(self) -> dict:
        pass

    @staticmethod
    def _covert_shortcut(platform_dependent_shortcut: any) -> Shortcut:
        pass
