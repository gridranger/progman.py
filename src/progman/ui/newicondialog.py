from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from tkinter import Button, Entry, Frame, Label, StringVar, Tk, Toplevel
from tkinter.constants import DISABLED, END, HORIZONTAL, NORMAL
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import Dialog
from tkinter.ttk import Combobox, Separator
from typing import Literal

from assets import asset_storage
from core import Shortcut
from platforms import IconLoader
from ui.progmanwidgets import ProgmanWidget


@dataclass
class ButtonData:
    label: str
    command: Callable
    row: int
    state: Literal["active", "normal", "disabled"] = "normal"


class NewIconDialog(Dialog, ProgmanWidget):
    """Dialogs __init__ is dropped in favor of its ancestor's one.
        Reason: The body frame should grid geometry manager rather than pack.
    """

    def __init__(self, parent: Tk, title: str) -> None:
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
        self._icon_path = ""
        self._icon_preview = None
        self._selected_group = StringVar()
        self._program_group_label = None
        self._program_group_dropdown = None
        self._ok_button = None
        self._cancel_button = None
        self._browse_button = None
        self._change_icon_button = None
        self._eyes = "👀"
        self._okay = "👍"
        self._nokay = "🚫"
        self._font = ("Segoe UI Emoji",)
        self._validity = {"name": False, "target": False, "workdir": False}
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
    def _setup_dialog(self) -> None:
        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style", self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes(type="dialog")

    def _place_window(self, parent: Tk = None) -> None:
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
        self.wm_geometry('+%d+%d' % (x, y))  # noqa: UP031
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
        self._arguments_input = self._get_input(lambda new_value: True, "focusout", 2)
        self._arguments_feedback = self._get_feedback_label(2, optional=True)
        self._working_directory_label = self._get_default_label("working_directory", 3)
        self._working_directory_input = self._get_input(self._validate_workdir_path, "focusout", 3)
        self._working_directory_feedback = self._get_feedback_label(3)
        self._program_group_label = self._get_default_label("program_group", 4)
        options = list(self.app_state.groups.keys())
        self._program_group_dropdown = Combobox(self._settings_frame, textvariable=self._selected_group, values=options,
                                                width=37)
        self._program_group_dropdown.grid(column=1, row=4, **self._basic_kwargs)
        self._icon_preview = Label(self._settings_frame, image=asset_storage["new"], bg=self.theme.background)
        self._icon_preview.grid(column=0, row=5, **self._basic_kwargs)
        self._settings_frame.grid(column=0, row=0, **self._basic_kwargs)
        return self._name_input

    def _render_icon(self) -> None:
        self._icon = asset_storage[self._icon_name]
        self.iconphoto(False, self._icon)

    def _validate_name(self, new_value: str) -> bool:
        stripped_new_value = new_value.strip()
        if len(stripped_new_value) > 64:
            self._name_feedback.config(text=self._nokay)
            validity = True
            result = False
        elif (len(new_value) and not len(stripped_new_value)):
            validity = result = False
        elif len(stripped_new_value):
            self._name_feedback.config(text=self._okay)
            validity = result = True
        else:
            self._name_feedback.config(text=self._eyes)
            validity = False
            result = True
        self._validity["name"] = validity
        self._update_ok_button()
        return result

    def _update_ok_button(self) -> None:
        if all([value for value in self._validity.values()]):
            self._ok_button.configure(state=NORMAL)
        else:
            self._ok_button.configure(state=DISABLED)

    def _validate_target_path(self, new_value: str) -> bool:
        if '"' in new_value:
            cleaned_value = new_value.replace('"', "")
            self._target_path_input.delete(0, END)
            self._target_path_input.insert(0, cleaned_value)
            return self._validate_target_path(cleaned_value)
        okay_validity = False
        field_validity = False
        stripped_new_value = new_value
        value_as_path = Path(stripped_new_value)
        if not len(stripped_new_value):
            self._target_path_feedback.config(text=self._eyes)
            field_validity = True
        elif value_as_path.is_file():
            self._target_path_feedback.config(text=self._okay)
            self._load_icon(str(value_as_path))
            okay_validity = True
            field_validity = True
        else:
            self._target_path_feedback.config(text=self._nokay)
        self._validity["target"] = okay_validity
        self._update_ok_button()
        return field_validity

    def _validate_workdir_path(self, new_value: str) -> bool:
        if '"' in new_value:
            cleaned_value = new_value.replace('"', "")
            self._working_directory_input.delete(0, END)
            self._working_directory_input.insert(0, cleaned_value)
            return self._validate_workdir_path(cleaned_value)
        okay_validity = False
        field_validity = False
        stripped_new_value = new_value
        value_as_path = Path(stripped_new_value)
        if not len(stripped_new_value):
            self._working_directory_feedback.config(text=self._eyes)
            field_validity = True
        elif value_as_path.is_dir():
            self._working_directory_feedback.config(text=self._okay)
            okay_validity = True
            field_validity = True
        else:
            self._target_path_feedback.config(text=self._nokay)
        self._validity["workdir"] = okay_validity
        self._update_ok_button()
        return field_validity

    def _get_default_label(self, key: str, row: int) -> Label:
        new_label = Label(self._settings_frame, text=self.get_label(key),
                          bg=self.theme.background, fg=self.theme.foreground)
        new_label.grid(column=0, row=row, sticky="w", **self._basic_kwargs)
        return new_label

    def _get_input(self, validation_method: Callable, validate: Literal["key", "focusout"], row: int) -> Entry:
        new_input = Entry(self._settings_frame, bg=self.theme.background, fg=self.theme.foreground, width=40,
                          validate=validate, validatecommand=(self.register(validation_method), "%P"))
        new_input.grid(column=1, row=row, **self._basic_kwargs)
        return new_input

    def _get_feedback_label(self, row: int, optional: bool = False) -> Label:
        content = self._okay if optional else self._eyes
        new_label = Label(self._settings_frame, text=content, bg=self.theme.background, font=self._font)
        new_label.grid(column=2, row=row, **self._basic_kwargs)
        return new_label

    def buttonbox(self) -> None:
        buttons = [
            ButtonData("ok", self.ok, 0, DISABLED),
            ButtonData("cancel", self.cancel, 1),
            ButtonData("browse", self._browse_target, 3),
            ButtonData("change_icon", self._browse_icon, 4)
        ]
        self._button_box = Frame(self, bg=self.theme.background)
        separator = Separator(self._button_box, orient=HORIZONTAL)
        separator.grid(column=0, row=2, padx=10, pady=5, sticky='ew')
        for button in buttons:
            self._generate_button(button)
        self._button_box.grid(column=1, row=0, **self._basic_kwargs, sticky="n")

    def _generate_button(self, data: ButtonData) -> None:
        new_button = Button(self._button_box, text=self.get_label(data.label), width=12, command=data.command,
                            state=data.state, bg=self.theme.button_surface, fg=self.theme.foreground)
        new_button.grid(column=0, row=data.row, padx=5, pady=5)
        setattr(self, f"_{data.label}_button", new_button)

    def _browse_target(self) -> None:
        target_path = askopenfilename(defaultextension=".*", filetypes=[(self.get_label("all_files"), "*.*")])
        if target_path:
            self._target_path_input.delete(0, END)
            target_as_path_object = Path(target_path)   # Path(target_path) will show '\' in the path in Windows instead of '/' that python would use natively.
            self._target_path_input.insert(0, target_as_path_object)
            self._validate_target_path(str(target_as_path_object))
            if self._working_directory_input.get() == "":
                self._working_directory_input.insert(0, target_as_path_object.parent)
                self._validate_workdir_path(str(target_as_path_object.parent))
            if self._name_input.get() == "":
                new_name = target_as_path_object.name
                if new_name.lower().endswith(".exe"):
                    new_name = new_name[:-4]
                self._name_input.insert(0, new_name)
                self._validate_name(new_name)
            self._load_icon(target_path)

    def _load_icon(self, path: str) -> None:
        icon = IconLoader.load(path)
        asset_storage.store_icon(path, 0, icon)
        self._icon_preview.configure(image=icon)

    def _browse_icon(self) -> None:
        extensions = [
            ("Icon", "*.ico"),
            ("PNG", "*.png"),
            ("JPG", "*.jpg"),
            ("JPEG", "*.jpeg"),
            ("BMP", "*.bmp"),
            (self.get_label("all_files"), "*.*")
        ]
        icon_path = askopenfilename(defaultextension=".*", filetypes=extensions)
        if icon_path:
            self._icon_path = icon_path
            self._load_icon(icon_path)

    def validate(self) -> bool:
        return all([value for value in self._validity.values()])

    def apply(self) -> None:
        self.result = Shortcut(
            target_path=self._target_path_input.get().strip(),
            arguments=self._arguments_input.get().strip(),
            workdir_path=self._arguments_input.get().strip(),
            separate_icon_path=self._icon_path,
            name=self._name_input.get().strip(),
            created_by_user=True,
            tags=[self._selected_group.get()]
        )
