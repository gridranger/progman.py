from dataclasses import dataclass
from pathlib import Path


@dataclass
class Shortcut:
    target_path: str
    arguments: str
    workdir_path: str
    icon_path: str
    name: str = ""
    link_path: str = ""
    description: str = ""
    hotkey: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            if self.link_path:
                self.name = Path(self.link_path).stem
            else:
                self.name = Path(self.target_path).stem

    @property
    def launch_command(self) -> list[str]:
        return [self.target_path] + self.arguments.split()

    def to_dict(self) -> dict[str, str]:
        return {
            "target_path": self.target_path,
            "arguments": self.arguments,
            "workdir_path": self.workdir_path,
            "icon_path": self.icon_path,
            "name": self.name,
            "link_path": self.link_path,
            "description": self.description,
            "hotkey": self.hotkey
        }

    def __eq__(self, other: "Shortcut") -> bool:
        return (self.target_path == other.target_path and
                self.arguments == other.arguments and
                self.workdir_path == other.workdir_path)
