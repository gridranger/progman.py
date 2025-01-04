from json import load, dump
from os import getenv
from pathlib import Path
from platform import system

from core import Savable, State


class DataHandler:

    def __init__(self, state: State) -> None:
        self._state = state
        self._last_saved_state = {}

    @property
    def _settings_folder_path(self) -> Path:
        if system().lower() == "windows":
            return Path(getenv("LOCALAPPDATA")).joinpath("Progman")
        else:
            return Path.home().joinpath(".progman")

    @property
    def _file_path(self) -> Path:
        return self._settings_folder_path.joinpath("settings.json")

    def _find_settings_folder(self):
        if not self._settings_folder_path.exists():
            self._settings_folder_path.mkdir(exist_ok=True, parents=True)

    def load(self) -> None:
        if not self._settings_folder_path.exists() or not self._file_path.exists():
            return
        with open(self._file_path, "r") as file_handler:
            self._last_saved_state = load(file_handler)
        self._load_state()

    def _load_state(self) -> None:
        # Load theme
        # Load language
        for group in self._last_saved_state["groups"]:
            self._state.add_group(group)


    def save(self) -> None:
        save_state = self._create_save_state()
        if save_state == self._last_saved_state:
            return
        self._find_settings_folder()
        with open(self._file_path, "w") as file_handler:
            dump(save_state, file_handler, indent=4, ensure_ascii=False)

    def _create_save_state(self) -> dict:
        return {
            "theme": self._state.theme.name,
            "language": self._state.language.content["language"],
            "groups": [self._serialize(group) for group in self._state.groups.values()],
            "shortcuts": [self._serialize(shortcut) for shortcut in self._state.shortcuts]
        }

    @staticmethod
    def _serialize(item: Savable) -> dict:
        result = {}
        for field in item.FIELDS_TO_SAVE:
            result[field] = getattr(item, field)
        return result
