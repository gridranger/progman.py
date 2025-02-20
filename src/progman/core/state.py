from core.group import Group
from core.language import Language
from core.shortcut import Shortcut
from core.tags import HIDDEN_TAGS, Tags
from core.theme import Theme


class State:

    def __init__(self) -> None:
        self.language: Language = Language()
        self.theme: Theme = Theme()
        self.shortcuts: list[Shortcut] = []
        self._groups: dict[str, Group] = {}
        self.group_windows = {}
        self.suspended_group_windows = {}
        self.main_window_geometry = ""

    @property
    def groups(self) -> dict[str, Group]:
        if not self._groups:
            for shortcut in self.shortcuts:
                for tag in shortcut.tags:
                    self._groups.setdefault(tag, Group(tag)).append(shortcut)
            self._groups.setdefault(Tags.NEW.value, Group(Tags.NEW.value))
            self._groups.setdefault(Tags.HIDDEN.value, Group(Tags.HIDDEN.value))
        return self._groups

    @property
    def public_groups(self) -> list[str]:
        groups = [group_name for group_name in self._groups if group_name not in HIDDEN_TAGS]
        groups.sort()
        return groups

    def add_group(self, group: Group) -> None:
        geometry = f"{group.size[0]}x{group.size[1]}+{group.position[0]}+{group.position[1]}"
        self._groups[group.name] = Group(group.name, group.is_collapsed, geometry)

    def add_shortcut(self, new_item: Shortcut) -> None:
        self.shortcuts.append(new_item)
        for tag in new_item.tags:
            if tag != Tags.NEW.value:
                group = self.group_windows[tag]
                group.add_icon(new_item)
            self._groups[tag].append(new_item)

    def copy_shortcut_to_new_group(self, shortcut: Shortcut, group: str) -> None:
        shortcut.tags.append(group)
        shortcut.managed_by_user = True
        self._groups[group].append(shortcut)
        if group in self.group_windows:
            self.group_windows[group].add_icon(shortcut)

    def unhide_shortcut(self, shortcut: Shortcut, new_group: str) -> None:
        current_hidden_group = shortcut.tags[0]
        self._groups[current_hidden_group].shortcuts.remove(shortcut)
        shortcut.tags = [new_group]
        shortcut.managed_by_user = True
        self.add_shortcut(shortcut)
