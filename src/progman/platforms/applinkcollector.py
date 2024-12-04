from abc import ABC, abstractmethod


class AppLinkCollector(ABC):

    @abstractmethod
    def collect_links(self) -> dict:
        pass
