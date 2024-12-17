from pathlib import Path
from winreg import HKEY_CLASSES_ROOT, OpenKey, QueryValueEx

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from win32api import GetSystemMetrics
from win32con import SM_CXICON
from win32gui import DestroyIcon, ExtractIconEx, GetDC
from win32ui import CreateBitmap, CreateDCFromHandle

from progman.assets import asset_storage
from progman.core import Shortcut


class WindowsIconLoader:

    @classmethod
    def load(cls, shortcut: Shortcut) -> PhotoImage:
        path = Path(shortcut.icon)
        extension = path.suffix.lower()[1:]
        resolver_name = f"_load_from_{extension}"
        if hasattr(cls, resolver_name):
            result = getattr(cls, resolver_name)(shortcut.icon, shortcut.icon_index)
        else:
            result = cls._load_icon_from_default_app(shortcut.icon, shortcut.icon_index)
        return result

    @staticmethod
    def _load_from_exe(path: str, icon_index: int) -> PhotoImage:
        image_cache = asset_storage.get_icon(path, icon_index)
        if image_cache:
            return image_cache
        size = GetSystemMetrics(SM_CXICON)
        normal, _ = ExtractIconEx(path, icon_index)
        if _:
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

    @classmethod
    def _load_from_dll(cls, path: str, icon_index: int = 0) -> PhotoImage:
        return cls._load_from_exe(path, icon_index)

    @staticmethod
    def _load_from_ico(path: str, icon_index: int = 0) -> PhotoImage:
        image_cache = asset_storage.get_icon(path, icon_index)
        if image_cache:
            return image_cache
        image = Image.open(path)
        resized_image = image.resize((32, 32))
        icon = PhotoImage(resized_image)
        asset_storage.store_icon(path, icon_index, icon)
        return icon

    @classmethod
    def _load_icon_from_default_app(cls, path: str, icon_index: int) -> PhotoImage:
        extension = Path(path).suffix
        image_cache = asset_storage.get_icon(extension, icon_index)
        if image_cache:
            return image_cache
        with OpenKey(HKEY_CLASSES_ROOT, extension) as key:
            prog_id, _ = QueryValueEx(key, "")
        with OpenKey(HKEY_CLASSES_ROOT, prog_id) as prog_id_key:
            try:
                with OpenKey(prog_id_key, "DefaultIcon") as icon_key:
                    icon_path, _ = QueryValueEx(icon_key, "")
                    if ',' in icon_path:
                        file, icon_id = icon_path.split(",")
                    else:
                        file = icon_path
                        icon_id = 0
                    file = file.replace("%1", path)
                    loaded_icon = cls._load_from_exe(file, int(icon_id))
                    asset_storage.store_icon(extension, icon_index, loaded_icon)
                    return loaded_icon
            except FileNotFoundError:
                return asset_storage["blank"]
