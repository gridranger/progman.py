from assets import asset_storage
from core import Shortcut
from PIL.ImageTk import PhotoImage


class LinuxIconLoader:

    @classmethod
    def load(cls, shortcut: Shortcut | str) -> PhotoImage:
        try:
            if shortcut.startswith("/"):
                return asset_storage[shortcut]
        except AttributeError:
            return asset_storage[shortcut.icon]
