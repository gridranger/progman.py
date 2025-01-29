from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal


@dataclass
class MenuItem:
    label: str
    command: Callable = lambda: None
    state: Literal["normal", "disabled"] = "normal"
    toggle: bool = False
    type: Literal["command", "submenu"] = "command"

    def __post_init__(self):
        self.type = "separator" if self.label == "separator" else self.type
