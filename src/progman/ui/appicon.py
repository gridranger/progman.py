from functools import partial
from subprocess import Popen
from tkinter import Event, PhotoImage
from tkinter.constants import DISABLED

from core import MenuItem, Shortcut
from platforms import IconLoader
from ui.icon import Icon
from ui.iconpropertiesdialog import IconPropertiesDialog


class AppIcon(Icon):

    def __init__(self, shortcut: Shortcut, *args: any, **kwargs: any) -> None:
        Icon.__init__(self, *args, **kwargs)
        self._shortcut = shortcut
        self._menu_items = [
            MenuItem("copy_to", state=DISABLED, type="submenu"),
            MenuItem("move_to", state=DISABLED, type="submenu"),
            MenuItem("delete", command=self.delete_icon),
            MenuItem("separator"),
            MenuItem("properties", command=self.edit_properties),
        ]
        self._last_keys = set()

    def shortcut(self) -> Shortcut:
        return self._shortcut

    @property
    def icon(self) -> PhotoImage:
        if self._icon is None:
            self._icon = IconLoader.load(self._shortcut)
        return self._icon

    @property
    def _label(self) -> str:
        if len(self._shortcut.name) > 20:
            return self._shortcut.name[:17] + "..."
        return self._shortcut.name

    def _launch(self) -> None:
        Popen(self._shortcut.launch_command)

    def rename(self) -> None:
        self._text_label.configure(text=self._label)

    def edit_properties(self) -> None:
        dialog = IconPropertiesDialog(self, "edit_icon", self._shortcut)
        if dialog.result:
            self._process_shortcut_update(dialog.result)

    def _process_shortcut_update(self, new_shortcut: Shortcut) -> None:
        any_changes = False
        if new_shortcut.name != self._shortcut.name:
            self._shortcut.name = new_shortcut.name
            self.rename()
            any_changes = True
        if new_shortcut.target_path != self._shortcut.target_path:
            self._shortcut.target_path = new_shortcut.target_path
            any_changes = True
        if new_shortcut.arguments != self._shortcut.arguments:
            self._shortcut.arguments = new_shortcut.arguments
            any_changes = True
        if new_shortcut.workdir_path != self._shortcut.workdir_path:
            self._shortcut.workdir_path = new_shortcut.workdir_path
            any_changes = True
        if new_shortcut.separate_icon_path != self._shortcut.separate_icon_path:
            self._shortcut.separate_icon_path = new_shortcut.separate_icon_path
            self._update_icon()
            any_changes = True
        if new_shortcut.tags[0] not in self._shortcut.tags:
            self._update_tags(new_shortcut.tags[0])
            any_changes = True
        if any_changes:
            self._shortcut.created_by_user = True

    def _update_icon(self) -> None:
        self._icon = None
        self._icon_label.configure(image=self.icon)

    def _update_tags(self, new_tag: str) -> None:
        self._shortcut.tags.append(new_tag)
        self.app_state.add_shortcut_to_new_group(self._shortcut)

    def delete_icon(self) -> None:
        self.drawer.delete_icon(self, self._shortcut)

    def show_context_menu(self, event: Event) -> None:
        if self.app_state.public_groups != self._last_keys:
            for key in self._last_keys:
                self._sub_menus["move_to"].delete(key)
                self._sub_menus["copy_to"].delete(key)
            for key in self.app_state.public_groups:
                self._sub_menus["move_to"].add_command(label=key, command=partial(self._move_to_group, key), state=DISABLED)
                self._sub_menus["copy_to"].add_command(label=key, command=partial(self._move_to_group, key), state=DISABLED)
        Icon.show_context_menu(self, event)

    def _move_to_group(self, group: str) -> None:
        print("move", group)

    def _copy_to_group(self, group: str) -> None:
        print("copy", group)
