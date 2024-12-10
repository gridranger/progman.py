from platform import system

if system().lower() == "windows":
    from .windowsiconloader import WindowsIconLoader as IconLoader
    from .windowsshortcutcollector import WindowsShortcutCollector as ShortcutCollector
else:
    raise NotImplementedError


__all__ = ["IconLoader", "ShortcutCollector"]
