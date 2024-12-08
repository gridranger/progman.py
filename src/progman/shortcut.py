from dataclasses import dataclass, field
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
    created_by_user: bool = False
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            if self.link_path:
                self.name = Path(self.link_path).stem
            else:
                self.name = Path(self.target_path).stem

    @property
    def launch_command(self) -> list[str]:
        return [self.target_path] + self.arguments.split()

    def __eq__(self, other: "Shortcut") -> bool:
        return (self.target_path == other.target_path and
                self.arguments == other.arguments and
                self.workdir_path == other.workdir_path)
