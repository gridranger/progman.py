from pathlib import Path
from tkinter import PhotoImage


class AssetHandler:
    SUPPORTED_EXTENSIONS = ["png"]
    ASSETS = Path(__file__).parent
    BLANK_PATH = "blank"

    def __init__(self) -> None:
        self._available_images = []
        for ext in self.SUPPORTED_EXTENSIONS:
            self._available_images.extend(self.ASSETS.glob(f"*{ext}"))
        self._blank = None
        self._content = {}

    def __getitem__(self, image_name: str) -> PhotoImage:
        if image_name not in self._content:
            for current_image_name in self._available_images:
                name = Path(current_image_name).stem
                if name == image_name:
                    self._content[image_name] = PhotoImage(file=current_image_name)
                    break
            else:
                if self._blank is None:
                    self._blank = self["blank"]
                self._content[image_name] = self._blank
        return self._content[image_name]

    def get_icon(self, key: str, icon_id: int) -> PhotoImage | None:
        key = f"{key}-{icon_id}"
        return self._content.get(key, None)

    def store_icon(self, key: str, icon_id: int, image: PhotoImage) -> None:
        key = f"{key}-{icon_id}"
        if self._content.get(key):
            raise ResourceDuplicationError("No resource should be loaded twice!")
        self._content[key] = image


class ResourceDuplicationError(RuntimeError):
    pass
