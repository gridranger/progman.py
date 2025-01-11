from tkinter import ACTIVE, LEFT, Button, Entry, Frame, Label
from tkinter.simpledialog import Dialog

from assets import asset_storage
from ui.progmanwidgets import ProgmanWidget


class NewGroupDialog(Dialog, ProgmanWidget):

    def __init__(self, *args: any, **kwargs: any) -> None:
        ProgmanWidget.__init__(self, "new_group_window")
        self._icon_name = "blank"
        self._input_box = None
        self._label = None
        self._input_field = None
        self._lava_lamp = None
        self._button_box = None
        self._okay_button = None
        self._cancel_button = None
        Dialog.__init__(self, *args, **kwargs)

    def body(self, master: Frame) -> Entry:
        self._render_title()
        self._render_icon()
        self._input_box = Frame(self, bg=self.theme.background)
        self._label = Label(self._input_box, text=self.get_label("name"),
                            bg=self.theme.background, fg=self.theme.foreground)
        self._label.pack(side=LEFT, padx=5, pady=5)
        self._input_field = Entry(self._input_box, bg=self.theme.background, fg=self.theme.foreground, validate="key",
                                  validatecommand=(self.register(self._control_lava_lamp), "%P"))
        self._input_field.pack(side=LEFT, padx=5, pady=5)
        self._lava_lamp = Label(self._input_box, text="👀", bg=self.theme.background, font=("Arial",))
        self._lava_lamp.pack(side=LEFT, padx=5, pady=5)
        self._input_box.pack()
        self.configure(bg=self.theme.background)
        self._input_box.configure()
        self._label.configure()
        return self._input_field

    def buttonbox(self) -> None:
        self._button_box = Frame(self, bg=self.theme.background)
        self._ok_button = Button(self._button_box, text=self.get_label("ok"), width=10, command=self.ok, default=ACTIVE,
                                 bg=self.theme.background, fg=self.theme.foreground)
        self._ok_button.pack(side=LEFT, padx=5, pady=5)
        self._cancel_button = Button(self._button_box, text=self.get_label("cancel"), width=10, command=self.cancel,
                                     bg=self.theme.background, fg=self.theme.foreground)
        self._cancel_button.pack(side=LEFT, padx=5, pady=5)
        self._button_box.pack()
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def _control_lava_lamp(self, new_value: str) -> bool:
        if new_value.lower() in [g.lower() for g in self.app_state.groups]:
            self._lava_lamp.config(text="🚫")
            return True
        if not new_value:
            self._lava_lamp.config(text="👀")
            return True
        self._lava_lamp.config(text="👍")
        return True

    def validate(self) -> bool:
        value = self._input_field.get()
        if not value or value.lower() in [g.lower() for g in self.app_state.groups]:
            return False
        return True

    def apply(self) -> None:
        self.result = self._input_field.get()

    def _render_title(self) -> None:
        self._set_title()
        self._texts["title"].trace("w", self._set_title)

    def _set_title(self) -> None:
        self.title(self.get_label("title"))

    def _render_icon(self) -> None:
        self._icon = asset_storage[self._icon_name]
        self.iconphoto(False, self._icon)
