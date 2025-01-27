from core.shortcut import Shortcut
from core.tags import Tags


class Recognizer:
    negative_name_hints = [
        "About Java", "App Recovery",
        "Check For Updates", "Compatibility Mode", "Configure Java",
        "EA app Updater", "EA Error Reporter", "EA Updater",
        "Git Release Notes",
        "Manuals", "Module Docs",
        "Node.js", "nvm",
        "Start Service", "Stop Service",
        "VLC media player - reset preferences and cache files", "VLC media player skinned", "VLC Setup Helper",
        "Wacom Tablet Properties", "Wacom Update Utility", "Windows Software Development Kit"
    ]
    negative_extension_filter = [".url", ".txt", ".chm", ".ico"]
    negative_path_hints = [
        "sapisvr", "setlang", "system32", "syswow64",
        "unins", "unin64",
        "windows kits"
    ]
    name_hints = {
        Tags.ACCESSORIES: [
            "7-Zip",
            "Acrobat", "Auto Dark Mode",
            "Angry IP Scanner",
            "Double Commander",
            "File Explorer",
            "GeForce",
            "Hard Disk Sentinel",
            "ImgBurn",
            "Logi Options", "Logi Plugin",
            "Notepad",
            "Pi Imager",
            "PowerShell",
            "Registry Editor",
            "Speech Recognition", "Sticky Notes",
            "Total Commander",
            "Wordpad"
        ],
        Tags.CREATIVITY: [
            "GIMP",
            "Inkscape", "Inkview",
            "Obsidian",
            "Shotcut",
            "Typora",
            "Wacom Center"
        ],
        Tags.DEVELOPMENT: [
            "Emacs",
            "IDLE",
            "PhpStorm", "PyCharm", "Python",
            "Visual Studio", "VSCod",
            "WebStorm",
            "Wireshark"
        ],
        Tags.GAMES: [
            "Epic Games",
            "Steam",
            "Ubisoft Connect",
            "Vortex"
        ],
        Tags.INTERNET: [
            "Chrom",
            "Discord",
            "Edge",
            "qBitt",
            "Teams",
            "Viber",
            "Zoom"
        ],
        Tags.MULTIMEDIA: [
            "FreeTube",
            "Media Player",
            "VLC media player"
        ],
        Tags.OFFICE: [
            "Access",
            "Excel",
            "OneDrive", "OneNote", "Outlook",
            "PowerPoint",
            "Publisher",
            "Word"
        ]
    }
    path_hints = {
        Tags.ACCESSORIES: [
            "Cooler Master",
        ],
        Tags.GAMES: [
            "EALauncher",
            "steamapps",
            "games", "Games"
        ]
    }

    @classmethod
    def categorize(cls, shortcut: Shortcut) -> None:
        if shortcut.tags:
            return
        if any([name_part in shortcut.name for name_part in cls.negative_name_hints]):
            shortcut.tags = [Tags.HIDDEN.value]
            return
        if any([shortcut.target_path.lower().endswith(extension) for extension in cls.negative_extension_filter]):
            shortcut.tags = [Tags.HIDDEN.value]
            return
        if any([path_part in shortcut.target_path.lower() for path_part in cls.negative_path_hints]):
            shortcut.tags = [Tags.HIDDEN.value]
            return
        for tag, path_hint_list in cls.path_hints.items():
            if any([path_hint in shortcut.target_path for path_hint in path_hint_list]):
                shortcut.tags = [tag.value]
                return
        for tag, name_hint_list in cls.name_hints.items():
            if any([name_hint in shortcut.name for name_hint in name_hint_list]):
                shortcut.tags = [tag.value]
                return
        shortcut.tags = [Tags.NEW.value]
