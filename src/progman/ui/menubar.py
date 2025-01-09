from tkinter import Menu

from ui.progmanwidgets import ProgmanWidget


class Menubar(Menu, ProgmanWidget):

    def __init__(self, *args: any, **kwargs: any) -> None:
        Menu.__init__(self, *args, **kwargs)
        ProgmanWidget.__init__(self, "menu_bar")
        self._menus = {}
        self._raw_menu_data = {
            "file": [
                {"label": "new_group", "command": self.master.save, "state": "disabled"},
                {"label": "new_icon", "command": self.master.save, "state": "disabled"},
                {"separator": True},
                {"label": "save", "command": self.master.save, "state": "normal"},
                {"separator": True},
                {"label": "exit", "command": self.quit, "state": "normal"}
            ]
        }

    def render(self) -> None:
        for menu_name, menu_data in self._raw_menu_data.items():
            self._menus[menu_name] = Menu(self, tearoff=0)
            for item in menu_data:
                if "separator" in item:
                    self._menus[menu_name].add_separator()
                else:
                    self._menus[menu_name].add_command(
                        label=self.get_label(item["label"]),
                        command=item["command"],
                        state=item["state"]
                    )
            self.add_cascade(label=self.get_label(menu_name), menu=self._menus[menu_name])


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
