from json import dump, load
from os import getenv
from pathlib import Path
from platform import system

from core import Language, Savable, Shortcut, State, Theme


class DataHandler:

    def __init__(self, state: State = None) -> None:
        self._state = state or State()
        self._last_saved_state = {}

    @property
    def _settings_folder_path(self) -> Path:
        if system().lower() == "windows":
            return Path(getenv("LOCALAPPDATA")).joinpath("Progman")
        return Path.home().joinpath(".progman")

    @property
    def _file_path(self) -> Path:
        return self._settings_folder_path.joinpath("settings.json")

    def _find_settings_folder(self) -> None:
        if not self._settings_folder_path.exists():
            self._settings_folder_path.mkdir(exist_ok=True, parents=True)

    def load(self) -> State:
        if not self._settings_folder_path.exists() or not self._file_path.exists():
            return State()
        with Path(self._file_path).open() as file_handler:
            self._last_saved_state = load(file_handler)
        return self._load_state()

    def _load_state(self) -> State:
        new_state = State()
        new_state.language = Language()  # TODO
        new_state.theme = Theme()  # TODO
        new_state.main_window_geometry = self._last_saved_state["groups"].pop("Program Manager")[0]
        new_state.shortcuts = [Shortcut(**shortcut) for shortcut in self._last_saved_state["shortcuts"]]
        new_state.suspended_group_windows = self._last_saved_state["groups"]
        return new_state

    def save(self) -> None:
        save_state = self._create_save_state()
        if save_state == self._last_saved_state:
            return
        self._find_settings_folder()
        with Path(self._file_path).open("w") as file_handler:
            dump(save_state, file_handler, indent=4, ensure_ascii=False)

    def _create_save_state(self) -> dict:
        return {
            "theme": self._state.theme.name,
            "language": self._state.language.content["language"],
            "groups": self._serialize_groups(),
            "shortcuts": [self._serialize(shortcut) for shortcut in self._state.shortcuts]
        }

    @staticmethod
    def _serialize(item: Savable) -> dict:
        result = {}
        for field in item.FIELDS_TO_SAVE:
            field_name = field.replace("_as_string", "")
            result[field_name] = getattr(item, field)
        return result

    def _serialize_groups(self) -> dict[str, tuple[str, bool]]:
        result = {"Program Manager": (self._state.main_window_geometry, True)}
        for group_window in self._state.group_windows.values():
            result[group_window.group_name] = (group_window.geometry(), True)
        for group_name, geometry in self._state.suspended_group_windows.items():
            result[group_name] = (geometry, False)
        return result
