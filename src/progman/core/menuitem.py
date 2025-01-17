from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal


@dataclass
class MenuItem:
    label: str
    command: Callable = lambda: None
    state: Literal["normal", "disabled"] = "normal"
    toggle: bool = False
