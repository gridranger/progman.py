from pathlib import Path
from tkinter import Tk, Label
from winreg import OpenKey, HKEY_CLASSES_ROOT, QueryValue, QueryValueEx
from PIL import Image
from PIL.ImageTk import PhotoImage

from progman.platforms.windowsiconloader import WindowsIconLoader

def test_load_exe_and_dll():
    # Example usage
    root = Tk()
    root.title("Display Icon")
    # exe_path = r"C:\Program Files\Typora\Typora.exe"
    exe_path = r"C:\WINDOWS\system32\shell32.dll"
    icon = WindowsIconLoader()._load_from_exe(exe_path, -25)
    label = Label(root, image=icon)
    label.pack(pady=20, padx=20)
    root.mainloop()

def test_load_ico_and_multi_ico():
    root = Tk()
    root.title("Display Icon")
    ico_path = r"C:\Program Files\Git\mingw64\share\git\git-for-windows.ico"
    icon = WindowsIconLoader()._load_from_ico(ico_path, 0)
    label = Label(root, image=icon)
    label.pack(pady=20, padx=20)
    root.mainloop()

def get_default_app(path: str):
    extension = Path(path).suffix
    with OpenKey(HKEY_CLASSES_ROOT, extension) as key:
        prog_id, _ = QueryValueEx(key, "")
    with OpenKey(HKEY_CLASSES_ROOT, prog_id) as prog_id_key:
        try:
            with OpenKey(prog_id_key, "DefaultIcon") as icon_key:
                icon_path, _ = QueryValueEx(icon_key, "")
                file, icon_id = icon_path.split(",")
                return WindowsIconLoader()._load_from_exe(file, int(icon_id))
        except FileNotFoundError:

            return PhotoImage(Image.open(r"C:\Users\bardo\repos\progman\src\progman\assets\blank.png"))


def test_load_txt():
    root = Tk()
    root.title("Display Icon")
    path = r"C:\Users\bardo\OneDrive\Desktop\foo.txt"
    icon = get_default_app(path)
    label = Label(root, image=icon)
    label.pack(pady=20, padx=20)
    root.mainloop()