from tkinter import Event, Tk

from core import State
from ui.groupdrawer import GroupDrawer
from ui.iconpropertiesdialog import IconPropertiesDialog
from ui.menubar import Menubar
from ui.newgroupdialog import NewGroupDialog
from ui.progmanwidgets import ProgmanWidget
from ui.window import Window


class MainWindow(Tk, ProgmanWidget, Window):

    def __init__(self, state: State) -> None:
        Tk.__init__(self)
        self._state = state
        ProgmanWidget.__init__(self, "root")
        Window.__init__(self, "progman")
        self._menubar = None
        self._is_first_render = True
        self._run_test_hook = lambda: None

    # region Properties
    @property
    def app_state(self) -> State:
        return self._state

    @property
    def group_name(self) -> str:
        return "Program Manager"
    # endregion

    # region Display
    def render(self) -> None:
        Window.render(self)
        self._render_menubar()
        self.render_drawer()
        self.update_language()
        self.update_theme()
        ProgmanWidget.render(self)
        self._icon_drawer.set_initial_geometry()
        if self._is_first_render:
            self._execute_first_render_only_actions()

    def _render_title(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)

    def _render_menubar(self) -> None:
        self._menubar = Menubar(self)
        self.configure(menu=self._menubar)

    def render_drawer(self) -> None:
        Window.render_drawer(self)
        self._icon_drawer = GroupDrawer(self)

    def _set_title(self, *_args: any) -> None:
        self.title(self.get_label("title"))

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def _execute_first_render_only_actions(self) -> None:
        self.bind("<Map>", self._on_deiconify)
        self.bind("<Unmap>", self._on_iconify)
        self._icon_drawer.restore_last_windows()
        self._is_first_render = False
        self._run_test_hook()
    # endregion

    # region Actions
    def _on_iconify(self, event: Event) -> None:
        if event.widget == self:
            self._icon_drawer.minimize_child_windows()

    def _on_deiconify(self, event: Event) -> None:
        if event.widget == self:
            self._icon_drawer.restore_child_windows()
            self.focus_set()

    def update_configuration(self, event: Event) -> None:
        if event.widget == self:
            Window.update_configuration(self, event)
            corrected_geometry = f"{self.winfo_width()}x{self.winfo_height() + 20}+{self.winfo_x()}+{self.winfo_y()}"
            self.app_state.main_window_geometry = corrected_geometry

    def show_new_group_dialog(self) -> None:
        dialog = NewGroupDialog(self)
        if dialog.result:
            self._icon_drawer.create_new_group(dialog.result)

    def show_new_icon_dialog(self) -> None:
        dialog = IconPropertiesDialog(self, "new_icon")
        if dialog.result:
            self.app_state.add_shortcut(dialog.result)
    # endregion
