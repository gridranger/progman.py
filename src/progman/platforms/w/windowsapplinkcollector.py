from os import environ, walk
from os.path import exists, join
from win32com.client import Dispatch

from progman.platforms.applinkcollector import AppLinkCollector


class WindowsAppLinkCollector(AppLinkCollector):
    USER_START_MENU = join(environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs')
    COMMON_START_MENU = join(environ['PROGRAMDATA'], r'Microsoft\Windows\Start Menu\Programs')
    START_MENU_PATHS = [USER_START_MENU, COMMON_START_MENU]

    def collect_links(self) -> dict:
        links = {}
        link_list = self._list_start_menu_items()
        from json import dumps
        print(dumps(link_list, indent=2))
        return links

    def _list_start_menu_items(self) -> list[tuple[str, str]]:
        links = []
        for start_menu_path in self.START_MENU_PATHS:
            if exists(start_menu_path):
                for root, dirs, files in walk(start_menu_path):
                    for file in files:
                        if file.endswith('.lnk'):
                            shortcut_path = join(root, file)
                            target_path = self._get_shortcut_target(shortcut_path)
                            links.append((file[:-4], target_path))
        cleaned_link = self._clean_filter_links(links)
        return cleaned_link

    @staticmethod
    def _get_shortcut_target(path: str) -> str:
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(path)
        return shortcut.Targetpath

    @staticmethod
    def _clean_filter_links(link_list: list[tuple[str, str]]) -> list[tuple[str, str]]:
        path_filter = ["system32", "windows kits", "syswow64", "unins", "unin64"]
        extension_filter = [".url", ".txt", ".chm", ".ico"]
        path_rules = [
            lambda path: any([part in path.lower() for part in path_filter]),
            lambda path: any([path.lower().endswith(ext) for ext in extension_filter]),
            lambda path: "." not in path
        ]
        cleaned_list = []
        for name, path in link_list:
            if not any([rule(path) for rule in path_rules]):
                cleaned_list.append((name, path))
        return cleaned_list


if __name__ == "__main__":
    w = WindowsAppLinkCollector()
    w.collect_links()
