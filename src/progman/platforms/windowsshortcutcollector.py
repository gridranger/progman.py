from os import environ, getenv, walk
from pathlib import Path
from re import Match
from re import compile as re_compile

from win32com.client import Dispatch
from win32com.universal import com_error

from progman.core import Shortcut

from .shortcutcollector import ShortcutCollector


class WindowsShortcutCollector(ShortcutCollector):
    USER_START_MENU = Path(environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs')
    COMMON_START_MENU = Path(environ['PROGRAMDATA'], r'Microsoft\Windows\Start Menu\Programs')
    START_MENU_PATHS = [USER_START_MENU, COMMON_START_MENU]

    def collect_links(self) -> list:
        return self._list_start_menu_items()

    @staticmethod
    def _list_start_menu_items() -> list[Shortcut]:
        shortcuts = set()
        shell = Dispatch("WScript.Shell")
        for start_menu_path in WindowsShortcutCollector.START_MENU_PATHS:
            if Path.exists(start_menu_path):
                for root, dirs, files in walk(start_menu_path):
                    for file in files:
                        if file.endswith('.lnk'):
                            shortcut_path = Path(root, file)
                            shortcut = shell.CreateShortcut(str(shortcut_path))
                            common_shortcut = WindowsShortcutCollector._covert_shortcut(shortcut)
                            shortcuts.add(common_shortcut)
        shortcut_list = list(shortcuts)
        shortcut_list.sort(key=lambda item: item.name)
        return shortcut_list

    @staticmethod
    def _covert_shortcut(platform_dependent_shortcut: any) -> Shortcut:
        try:
            description = platform_dependent_shortcut.Description
        except com_error:
            description = ""
        raw_icon_path = WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.IconLocation)
        if ',' in raw_icon_path:
            icon_path, _, icon_index = raw_icon_path.partition(',')
            icon_index = int(icon_index)
        else:
            icon_path = raw_icon_path
            icon_index = 0
        return Shortcut(
            arguments=platform_dependent_shortcut.Arguments,
            description=description,
            link_path=WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.FullName),
            hotkey=platform_dependent_shortcut.Hotkey,
            separate_icon_path=icon_path, icon_index=icon_index,
            target_path=WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.TargetPath),
            workdir_path=WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.WorkingDirectory)
        )

    @staticmethod
    def resolve_env_vars(input_string: str) -> str:
        """Regular expression to find all %envvar% patterns"""
        pattern = re_compile(r'%([^%]+)%')
        return pattern.sub(WindowsShortcutCollector.replace_var, input_string)

    @staticmethod
    def replace_var(match: Match) -> str:
        var_name = match.group(1)
        return getenv(var_name, match.group(0))  # Return the env var value or the original string if not found
