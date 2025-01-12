from dataclasses import dataclass, field
from os import name
from pathlib import Path


@dataclass
class Shortcut:
    FIELDS_TO_SAVE = ["target_path", "arguments", "workdir_path", "separate_icon_path", "icon_index", "name",
                      "link_path", "description", "hotkey", "created_by_user", "tags"]

    target_path: str
    arguments: str
    workdir_path: str
    separate_icon_path: str
    icon_index: int = 0
    name: str = ""
    link_path: str = ""
    description: str = ""
    hotkey: str = ""
    created_by_user: bool = False
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            if self.link_path:
                self.name = Path(self.link_path).stem
            else:
                self.name = Path(self.target_path).stem

    @property
    def icon(self) -> str:
        is_protected = 'windows' in self.separate_icon_path.lower()
        if self.separate_icon_path and Path(self.separate_icon_path).exists() and not is_protected:
            return self.separate_icon_path
        if is_protected:
            self.icon_index = 0
        return self.target_path

    @property
    def launch_command(self) -> list[str]:
        return [self.target_path] + self.arguments.split()

    def __eq__(self, other: "Shortcut") -> bool:
        return (self.target_path == other.target_path and
                self.arguments == other.arguments and
                self.workdir_path == other.workdir_path)

    def __hash__(self) -> int:
        target_path = self.target_path.lower() if name == "nt" else self.target_path
        workdir_path = self.workdir_path.lower() if name == "nt" else self.workdir_path
        return hash(target_path + self.arguments + workdir_path)
