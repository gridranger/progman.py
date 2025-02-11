from tkinter import BooleanVar, Menu

from core import MenuItem
from ui.progmanwidgets import ProgmanWidget


class Menubar(Menu, ProgmanWidget):

    def __init__(self, *args: any, **kwargs: any) -> None:
        Menu.__init__(self, *args, **kwargs)
        ProgmanWidget.__init__(self, "menu_bar")
        self._menus = {}
        self._raw_menu_data = {
            "file": [
                MenuItem("new_group", self._new_group),
                MenuItem("new_icon", self._new_icon),
                MenuItem("separator"),
                MenuItem("save", self.master.save),
                MenuItem("separator"),
                MenuItem("exit", self.quit)
            ],
            "options": [
                MenuItem("minimize_on_use", self._toggle_minimize_on_use, "disabled", toggle=True),
                MenuItem("arrange_abc", self._toggle_arrange_alphabetically, "disabled", True),
                MenuItem("show_windows_on_tray", self._toggle_show_windows_on_tray, "disabled", True)
            ],
            "window": [
                MenuItem("cascade", state="disabled"),
                MenuItem("tile", state="disabled")
            ]
        }
        self._toggles = {}

    def render(self) -> None:
        for menu_name, menu_data in self._raw_menu_data.items():
            self._menus[menu_name] = Menu(self, tearoff=0)
            for item in menu_data:
                if item.toggle:
                    self._render_toggle(menu_name, item)
                else:
                    self._render_menu_item(menu_name, item)
            self.add_cascade(label=self.get_label(menu_name), menu=self._menus[menu_name])

    def _render_toggle(self, name: str, item: MenuItem) -> None:
        self._toggles["label"] = BooleanVar()
        self._menus[name].add_checkbutton(label=self.get_label(item.label), command=item.command, state=item.state,
                                                               onvalue=True, offvalue=False,
                                                               variable=self._toggles["label"])

    def _render_menu_item(self, name: str, item: MenuItem) -> None:
        if item.label == "separator":
            self._menus[name].add_separator()
        else:
            self._menus[name].add_command(label=self.get_label(item.label), command=item.command, state=item.state)

    def _set_file_menu_label(self, *_args: any) -> None:
        self.entryconfig(0, label=self.get_label("file"))
        self._menus["file"].entryconfig(0, label=self.get_label("new_group"))
        self._menus["file"].entryconfig(1, label=self.get_label("new_icon"))
        self._menus["file"].entryconfig(3, label=self.get_label("save"))
        self._menus["file"].entryconfig(5, label=self.get_label("exit"))

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def update_language(self) -> None:
        ProgmanWidget.update_language(self)

    def _new_group(self) -> None:
        self.master.show_new_group_dialog()

    def _new_icon(self) -> None:
        self.master.show_new_icon_dialog()

    def _toggle_minimize_on_use(self) -> None:
        pass

    def _toggle_arrange_alphabetically(self) -> None:
        pass

    def _toggle_show_windows_on_tray(self) -> None:
        pass
