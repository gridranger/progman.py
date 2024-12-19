from ..core.tags import Tags
from .groupicon import GroupIcon
from .icondrawer import IconDrawer
from .groupswindow import GroupsWindow


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
        child_window = GroupsWindow(self.master, group_name)
        child_window.render()
