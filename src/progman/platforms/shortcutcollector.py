from abc import ABC, abstractmethod

from core import Shortcut


class ShortcutCollector(ABC):

    @abstractmethod
    def collect_links(self) -> dict:
        pass

    @staticmethod
    def _covert_shortcut(platform_dependent_shortcut: any) -> Shortcut:
        pass
