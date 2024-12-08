from functools import cache
from pathlib import Path
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from win32api import GetSystemMetrics
from win32con import SM_CXICON
from win32gui import DestroyIcon, ExtractIconEx, GetDC
from win32ui import CreateBitmap, CreateDCFromHandle
from winreg import HKEY_CLASSES_ROOT, OpenKey, QueryValueEx

from ..assets import asset_storage
from ..shortcut import Shortcut


class WindowsIconLoader:

    def load(self, shortcut: Shortcut) -> PhotoImage:
        cleaned_icon_path = ""
        icon_index = 0
        if "," in shortcut.icon_path:
            cleaned_icon_path = shortcut.icon_path.split(",")[0]
            icon_index = int(shortcut.icon_path.split(",")[1])
        if not cleaned_icon_path:
            cleaned_icon_path = shortcut.icon_path or shortcut.target_path
        path = Path(cleaned_icon_path)
        extension = path.suffix.lower()
        resolver_name = f"_load_from_{extension}"
        if hasattr(self, resolver_name):
            result = getattr(self, resolver_name)(cleaned_icon_path, icon_index)
        else:
            result = self._load_icon_from_default_app(cleaned_icon_path, icon_index)
        return result

    @staticmethod
    def _load_from_exe(path: str, icon_index: int) -> PhotoImage:
        cache = asset_storage.get_icon(path, icon_index)
        if cache:
            return cache
        size = GetSystemMetrics(SM_CXICON)
        normal, _ = ExtractIconEx(path, icon_index)
        DestroyIcon(_[0])
        device_context = CreateDCFromHandle(GetDC(0))
        bitmap = CreateBitmap()
        bitmap.CreateCompatibleBitmap(device_context, size, size)
        memory_device_context = device_context.CreateCompatibleDC()
        memory_device_context.SelectObject(bitmap)
        memory_device_context.DrawIcon((0, 0), normal[0])
        bits = bitmap.GetBitmapBits(True)
        image = Image.frombuffer('RGBA', (32, 32), bits, 'raw', 'BGRA', 0, 1)
        icon = ImageTk.PhotoImage(image)
        asset_storage.store_icon(path, icon_index, icon)
        return icon

    def _load_from_dll(self, path: str, icon_index: int = 0) -> PhotoImage:
        return self._load_from_exe(path, icon_index)

    @staticmethod
    def _load_from_ico(path: str, icon_index: int = 0) -> PhotoImage:
        cache = asset_storage.get_icon(path, icon_index)
        if cache:
            return cache
        image = Image.open(path)
        resized_image = image.resize((32, 32))
        icon = PhotoImage(resized_image)
        asset_storage.store_icon(path, icon_index, icon)
        return icon

    def _load_icon_from_default_app(self, path: str, icon_index: int) -> PhotoImage:
        extension = Path(path).suffix
        cache = asset_storage.get_icon(extension, icon_index)
        if cache:
            return cache
        with OpenKey(HKEY_CLASSES_ROOT, extension) as key:
            prog_id, _ = QueryValueEx(key, "")
        with OpenKey(HKEY_CLASSES_ROOT, prog_id) as prog_id_key:
            try:
                with OpenKey(prog_id_key, "DefaultIcon") as icon_key:
                    icon_path, _ = QueryValueEx(icon_key, "")
                    file, icon_id = icon_path.split(",")
                    loaded_icon = WindowsIconLoader()._load_from_exe(file, int(icon_id))
                    asset_storage.store_icon(extension, icon_index, loaded_icon)
                    return loaded_icon
            except FileNotFoundError:
                return asset_storage["blank"]
