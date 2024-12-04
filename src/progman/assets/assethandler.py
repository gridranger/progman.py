from glob import glob
from os.path import basename, join, splitext
from tkinter import PhotoImage


class AssetHandler:
    SUPPORTED_EXTENSIONS = ["png"]
    BLANK_PATH = "blank"

    def __init__(self):
        self._available_images = []
        for ext in self.SUPPORTED_EXTENSIONS:
            self._available_images.extend(glob(join("assets", f"*{ext}")))
        self._blank = None
        self._content = {}

    def __getitem__(self, image_name: str) -> PhotoImage:
        if image_name not in self._content:
            for current_image_name in self._available_images:
                name, _extension = splitext(basename(current_image_name))
                if name == image_name:
                    self._content[image_name] = PhotoImage(file=current_image_name)
                    break
            else:
                if self._blank is None:
                    self._blank = self["blank"]
                self._content[image_name] = self._blank
        return self._content[image_name]
