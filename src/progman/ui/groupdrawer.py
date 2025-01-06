from core.tags import Tags
from ui.groupicon import GroupIcon
from ui.icondrawer import IconDrawer
from ui.groupwindow import GroupWindow


class GroupDrawer(IconDrawer):
    DISABLED_GROUPS = [Tags.HIDDEN.value, Tags.NEW.value]

    def __init__(self, parent: any) -> None:
        IconDrawer.__init__(self, parent)
        self.viewPort._launch_child_window = self._launch_child_window

    def _render_icons(self) -> None:
        for group_name, group in self.app_state.groups.items():
            if group_name in self.DISABLED_GROUPS or group.is_empty:
                continue
            icon = GroupIcon(self.viewPort, group_name)
            self._icons.append(icon)

    def _launch_child_window(self, group_name: str) -> None:
        if group_name in self.app_state.group_windows:
            self.app_state.group_windows[group_name].deiconify()
            self.app_state.group_windows[group_name].focus_set()
        else:
            self.app_state.group_windows[group_name] = GroupWindow(self.master, group_name)
            self.app_state.group_windows[group_name].render()

    def _store_configuration(self) -> None:
        pass  # self.app_state.groups["Program Manager"].set_geometry(self.geometry())

    def minimize_child_windows(self):
        for child_window in self.app_state.group_windows.values():
            child_window.iconify()

    def restore_child_windows(self):
        for child_window in self.app_state.group_windows.values():
            child_window.update_idletasks()
            child_window.deiconify()
