from .icon import GroupIcon
from .icondrawer import IconDrawer
from ..core.tags import Tags


class GroupDrawer(IconDrawer):
    DISABLED_GROUPS = [Tags.HIDDEN.value, Tags.NEW.value]

    def _render_icons(self):
        for group_name, group in self.state.groups.items():
            if group_name in self.DISABLED_GROUPS or group.is_empty:
                continue
            icon = GroupIcon(group_name)
            self._icons.append(icon)
