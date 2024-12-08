from os import environ, getenv, walk
from pathlib import Path
from re import Match
from re import compile as re_compile

from win32com.client import Dispatch
from win32com.universal import com_error

from .shortcutcollector import ShortcutCollector
from ..shortcut import Shortcut
from ..tags import Tags


class WindowsShortcutCollector(ShortcutCollector):
    USER_START_MENU = Path(environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs')
    COMMON_START_MENU = Path(environ['PROGRAMDATA'], r'Microsoft\Windows\Start Menu\Programs')
    START_MENU_PATHS = [USER_START_MENU, COMMON_START_MENU]

    def collect_links(self) -> list:
        start_menu_items = self._list_start_menu_items()
        self._set_basic_tags(start_menu_items)
        for i in start_menu_items:
            if Tags.HIDDEN.value not in i.tags:
                print(i)
        return start_menu_items

    @staticmethod
    def _list_start_menu_items() -> list[Shortcut]:
        shortcuts = []
        shell = Dispatch("WScript.Shell")
        for start_menu_path in WindowsShortcutCollector.START_MENU_PATHS:
            if Path.exists(start_menu_path):
                for root, dirs, files in walk(start_menu_path):
                    for file in files:
                        if file.endswith('.lnk'):
                            shortcut_path = Path(root, file)
                            shortcut = shell.CreateShortcut(str(shortcut_path))
                            common_shortcut = WindowsShortcutCollector._covert_shortcut(shortcut)
                            shortcuts.append(common_shortcut)
        return shortcuts

    @staticmethod
    def _covert_shortcut(platform_dependent_shortcut: any) -> Shortcut:
        try:
            description = platform_dependent_shortcut.Description
        except com_error:
            description = ""
        return Shortcut(
            arguments=platform_dependent_shortcut.Arguments,
            description=description,
            link_path=WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.FullName),
            hotkey=platform_dependent_shortcut.Hotkey,
            icon_path=WindowsShortcutCollector.resolve_env_vars(platform_dependent_shortcut.IconLocation),
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

    @staticmethod
    def _get_shortcut_target(path: str) -> str:
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(path)
        return shortcut.Targetpath

    @staticmethod
    def _set_basic_tags(shortcuts: list[Shortcut]) -> None:
        path_filter = ["system32", "windows kits", "syswow64", "unins", "unin64"]
        extension_filter = [".url", ".txt", ".chm", ".ico"]
        path_rules = [
            lambda path: any([part in path.lower() for part in path_filter]),
            lambda path: any([path.lower().endswith(ext) for ext in extension_filter]),
            lambda path: "." not in path
        ]
        for shortcut in shortcuts:
            shortcut.tags = [Tags.NEW.value]
            if any([path_rule(shortcut.target_path) for path_rule in path_rules]):
                shortcut.tags.append(Tags.HIDDEN.value)
