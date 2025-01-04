from platform import system
from platforms.datahandler import DataHandler

if system().lower() == "windows":
    from .windowsiconloader import WindowsIconLoader as IconLoader
    from .windowsshortcutcollector import WindowsShortcutCollector as ShortcutCollector
else:
    raise NotImplementedError


__all__ = ["DataHandler", "IconLoader", "ShortcutCollector"]
