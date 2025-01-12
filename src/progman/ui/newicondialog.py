from pathlib import Path
from tkinter import Entry, Frame, LEFT, Label, Button, Toplevel, ACTIVE
from tkinter.simpledialog import Dialog
from typing import Callable, Literal

from assets import asset_storage
from ui.progmanwidgets import ProgmanWidget


class NewIconDialog(Dialog, ProgmanWidget):
    """Dialogs __init__ is dropped in favor of its ancestor's one.
        Reason: The body frame should grid geometry manager rather than pack.
    """

    def __init__(self, parent, title: str) -> None:
        ProgmanWidget.__init__(self, "new_icon_window")
        Toplevel.__init__(self, parent)
        self._basic_kwargs = {"padx": 5, "pady": 5}
        self.parent = parent
        self.result = None
        self._role = title
        self._icon_name = "blank"
        self._settings_frame = None
        self._button_box = None
        self._name_label = None
        self._name_input = None
        self._name_feedback = None
        self._target_path_label = None
        self._target_path_input = None
        self._target_path_feedback = None
        self._arguments_label = None
        self._arguments_input = None
        self._arguments_feedback = None
        self._working_directory_label = None
        self._working_directory_input = None
        self._working_directory_feedback = None
        self._icon_preview_frame = None
        self._okay_button = None
        self._cancel_button = None
        self._browse_button = None
        self._change_icon_button = None
        self._eyes = "👀"
        self._okay = "👍"
        self._nokay = "🚫"
        self._font = ("Segoe UI Emoji",)
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.grid(**self._basic_kwargs)
        self.buttonbox()
        self.initial_focus = self if self.initial_focus is None else self.initial_focus
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self._place_window(parent)
        self.initial_focus.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    # region tkinter legacy
    def _setup_dialog(self):
        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style", self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes(type="dialog")

    def _place_window(self, parent=None):
        self.wm_withdraw()  # Remain invisible while we figure out the geometry
        self.update_idletasks()  # Actualize geometry information
        minwidth = self.winfo_reqwidth()
        minheight = self.winfo_reqheight()
        maxwidth = self.winfo_vrootwidth()
        maxheight = self.winfo_vrootheight()
        if parent is not None and parent.winfo_ismapped():
            x = parent.winfo_rootx() + (parent.winfo_width() - minwidth) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - minheight) // 2
            vrootx = self.winfo_vrootx()
            vrooty = self.winfo_vrooty()
            x = min(x, vrootx + maxwidth - minwidth)
            x = max(x, vrootx)
            y = min(y, vrooty + maxheight - minheight)
            y = max(y, vrooty)
            if self._windowingsystem == 'aqua':
                # Avoid the native menu bar which sits on top of everything.
                y = max(y, 22)
        else:
            x = (self.winfo_screenwidth() - minwidth) // 2
            y = (self.winfo_screenheight() - minheight) // 2
        self.wm_maxsize(maxwidth, maxheight)
        self.wm_geometry('+%d+%d' % (x, y))
        self.wm_deiconify()
    # endregion

    def body(self, master: Frame) -> Entry:
        self.configure(bg=self.theme.background)
        self.title(self.get_label(self._role))
        self._render_icon()
        self._settings_frame = Frame(self, bg=self.theme.background)
        self._name_label = self._get_default_label("name", 0)
        self._name_input = self._get_input(self._validate_name, "key", 0)
        self._name_feedback = self._get_feedback_label(0)
        self._target_path_label = self._get_default_label("target_path", 1)
        self._target_path_input = self._get_input(self._validate_target_path, "focusout", 1)
        self._target_path_feedback = self._get_feedback_label(1)
        self._arguments_label = self._get_default_label("arguments", 2)
        self._arguments_input = self._get_input(lambda new_value: True, "focusout",2)
        self._arguments_feedback = self._get_feedback_label(2, optional=True)
        self._working_directory_label = self._get_default_label("working_directory", 3)
        self._working_directory_input = self._get_input(self._validate_workdir_path, "focusout", 3)
        self._working_directory_feedback = self._get_feedback_label(3)
        self._settings_frame.grid(column=0, row=0, **self._basic_kwargs)
        return self._name_input

    def _render_icon(self) -> None:
        self._icon = asset_storage[self._icon_name]
        self.iconphoto(False, self._icon)

    def _validate_name(self, new_value: str) -> bool:
        stripped_new_value = new_value.strip()
        if len(stripped_new_value) > 64:
            self._name_feedback.config(text=self._nokay)
            return False
        elif (len(new_value) and not len(stripped_new_value)):
            return False
        if len(new_value):
            self._name_feedback.config(text=self._okay)
        else:
            self._name_feedback.config(text=self._eyes)
        return True

    def _validate_target_path(self, new_value: str) -> bool:
        return self._validate_path(new_value, self._target_path_feedback)

    def _validate_path(self, new_value: str, feedback_widget: Label):
        if not len(new_value):
            feedback_widget.config(text=self._eyes)
            return True
        value_as_path = Path(new_value)
        if value_as_path.exists():
            feedback_widget.config(text=self._okay)
            return True
        feedback_widget.config(text=self._nokay)
        return False

    def _validate_workdir_path(self, new_value: str) -> bool:
        return self._validate_path(new_value, self._working_directory_feedback)

    def _get_default_label(self, key: str, row: int) -> Label:
        new_label = Label(self._settings_frame, text=self.get_label(key),
                                 bg=self.theme.background, fg=self.theme.foreground)
        new_label.grid(column=0, row=row, sticky="w", **self._basic_kwargs)
        return new_label

    def _get_input(self, validation_method: Callable, validate: Literal["key", "focusout"], row: int) -> Entry:
        new_input = Entry(self._settings_frame, bg=self.theme.background, fg=self.theme.foreground,
                          validate=validate, validatecommand=(self.register(validation_method), "%P"))
        new_input.grid(column=1, row=row, **self._basic_kwargs)
        return new_input

    def _get_feedback_label(self, row: int, optional: bool = False) -> Label:
        content = self._okay if optional else self._eyes
        new_label = Label(self._settings_frame, text=content, bg=self.theme.background, font=self._font)
        new_label.grid(column=2, row=row, **self._basic_kwargs)
        return new_label

    def buttonbox(self) -> None:
        self._button_box = Frame(self, bg=self.theme.background)
        self._ok_button = Button(self._button_box, text=self.get_label("ok"), width=10, command=self.ok, default=ACTIVE,
                                 bg=self.theme.background, fg=self.theme.foreground)
        self._ok_button.grid(column=0, row=0, padx=5, pady=5)
        self._cancel_button = Button(self._button_box, text=self.get_label("cancel"), width=10, command=self.cancel,
                                     bg=self.theme.background, fg=self.theme.foreground)
        self._cancel_button.grid(column=0, row=1, padx=5, pady=5)
        self._button_box.grid(column=1, row=0)
