from dataclasses import dataclass
from typing import Callable, Literal


@dataclass
class MenuItem:
    label: str
    command: Callable = lambda: None
    state: Literal["normal", "disabled"] = "normal"
    toggle: bool = False
