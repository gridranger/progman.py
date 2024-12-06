from dataclasses import dataclass


@dataclass
class Shortcut:
    arguments: str
    description: str
    link_path: str
    hotkey: str
    icon_path: str
    target_path: str
    workdir_path: str
