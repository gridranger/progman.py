
from core import HIDDEN_TAGS, Group
from ui.groupicon import GroupIcon
from ui.groupwindow import GroupWindow
from ui.icondrawer import IconDrawer


class GroupDrawer(IconDrawer):

    def __init__(self, parent: any) -> None:
        IconDrawer.__init__(self, parent)
        self.viewPort.launch_child_window = self.launch_child_window

    def create_new_group(self, group_name: str) -> None:
        self.app_state.add_group(Group(group_name))
        self._add_icon(group_name)
        self._icons[-1].render()
        self._arrange_icons()

    def _render_icons(self) -> None:
        for group_name, group in self.app_state.groups.items():
            if group_name in HIDDEN_TAGS:
                continue
            self._add_icon(group_name)

    def _add_icon(self, group_name: str) -> None:
        icon = GroupIcon(self, self.viewPort, group_name)
        self._icons.append(icon)

    def launch_child_window(self, group_name: str) -> None:
        if group_name in self.app_state.group_windows:
            self.app_state.group_windows[group_name].deiconify()
            self.app_state.group_windows[group_name].focus_set()
        else:
            self.app_state.group_windows[group_name] = GroupWindow(self.master, group_name)
            self.app_state.group_windows[group_name].render()

    def minimize_child_windows(self) -> None:
        for child_window in self.app_state.group_windows.values():
            child_window.iconify()

    def restore_child_windows(self) -> None:
        for child_window in self.app_state.group_windows.values():
            child_window.update_idletasks()
            child_window.deiconify()

    def restore_last_windows(self) -> None:
        windows_to_restore = list(self.app_state.suspended_group_windows.items())
        self.app_state.suspended_group_windows = {}
        for group_name, restoration_data in windows_to_restore:
            geometry, should_be_restored = restoration_data
            self.app_state.suspended_group_windows[group_name] = geometry
            if should_be_restored:
                self.app_state.group_windows[group_name] = GroupWindow(self.master, group_name)
                self.app_state.group_windows[group_name].render()

    def set_initial_geometry(self) -> None:
        if self.app_state.main_window_geometry:
            self.master.geometry(self.app_state.main_window_geometry)
        else:
            self.set_default_geometry()
