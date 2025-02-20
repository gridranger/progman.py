from functools import partial
from tkinter import Event, Misc, Toplevel

from core import HIDDEN_TAGS, Group, MenuItem, Shortcut
from ui.appdrawer import AppDrawer
from ui.iconpropertiesdialog import IconPropertiesDialog
from ui.progmanwidgets import ProgmanWidget
from ui.window import Window


class GroupWindow(Toplevel, ProgmanWidget, Window):
    FIELDS_TO_SAVE = ["group_name", "geometry_as_string"]

    def __init__(self, parent: Misc | None, group_name: str, *args: any, **kwargs: any) -> None:
        Toplevel.__init__(self, parent, *args, **kwargs)
        ProgmanWidget.__init__(self, "window")
        Window.__init__(self, "group")
        self._group_name = group_name
        self._menu_items = [
            MenuItem("new_icon", self._create_new_icon),
            MenuItem("add_new", type="submenu"),
            MenuItem("add_hidden", type="submenu")
        ]
        self._group_hashes = dict([(tag, 0) for tag in HIDDEN_TAGS])

    @property
    def group_name(self) -> str:
        return self._group_name

    def render(self) -> None:
        Window.render(self)
        self.render_drawer()
        self.update_theme()
        ProgmanWidget.render(self)
        self._icon_drawer.set_initial_geometry()
        self.bind("<Destroy>", self._on_destroy)

    def _render_title(self) -> None:
        self.title(self._group_name)

    def render_drawer(self) -> None:
        Window.render_drawer(self)
        self._icon_drawer = AppDrawer(self, self._group_name)

    def _on_destroy(self, event: Event) -> None:
        if event.widget == self:
            self.app_state.group_windows.pop(self._group_name)
            self.app_state.suspended_group_windows[self._group_name] = self.geometry_as_string

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def add_icon(self, new_shortcut: Shortcut) -> None:
        self._icon_drawer.add_icon(new_shortcut)

    def _create_new_icon(self) -> None:
        dialog = IconPropertiesDialog(self, "new_icon", default_group=self._group_name)
        if dialog.result:
            self.app_state.add_shortcut(dialog.result)

    def show_context_menu(self, event: Event) -> None:
        for tag in HIDDEN_TAGS:
            if hash(self.app_state.groups[tag]) != self._group_hashes[tag]:
                self.delete_items_from_menu(self._sub_menus["add_" + tag.lower()])
                self._generate_group_menu(self.app_state.groups[tag], tag)
        Window.show_context_menu(self, event)

    def _generate_group_menu(self, group: Group, tag: str) -> None:
        sub_menu = f"add_{tag.lower()}"
        for shortcut in sorted(group.shortcuts, key=lambda x: x.name.lower()):
            name = f"{shortcut.name} ({shortcut.target_path})" if shortcut.target_path else shortcut.name
            self._sub_menus[sub_menu].add_command(label=name,
                                                  command=partial(self._add_hidden_tagged_shortcut, shortcut))
        self._group_hashes[tag] = hash(self.app_state.groups[tag])

    def _add_hidden_tagged_shortcut(self, shortcut: Shortcut) -> None:
        self.app_state.unhide_shortcut(shortcut, self._group_name)
