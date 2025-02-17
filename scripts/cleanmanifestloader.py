from pathlib import Path
from subprocess import run
from tkinter import Label, Tk

from PIL import Image, ImageTk


def get_powershell_output(command: str) -> str:
    process = run(command, capture_output=True, text=True, shell=True)
    return process.stdout.strip()


def get_icon_name(app_name: str) -> Path:
    command = f"""powershell "(Get-AppxPackage -Name {app_name} | Get-AppxPackageManifest).package.properties.logo" """
    return Path(get_powershell_output(command))


def get_install_path(app_name: str) -> Path:
    command = f"""powershell "(Get-AppxPackage -Name {app_name}).InstallLocation" """
    return Path(get_powershell_output(command))


def locate_icon(icon: Path, install_path: Path) -> Path:
    matches = install_path.glob(f"**/{icon.stem}*.png")
    # usually 3 matches (default, black, white), let's use default
    return list(matches)[0]


def show_icon(icon_path: Path) -> None:
    root = Tk()
    root.title("Display Icon")
    pil_image = Image.open(icon_path)
    tk_image = ImageTk.PhotoImage(pil_image)
    label = Label(root, image=tk_image)
    label.pack()
    root.mainloop()


def main(current_name: str) -> None:
    icon_path = get_icon_name(current_name)
    print(icon_path)
    # Assets\CalculatorStoreLogo.png

    install_path = get_install_path(current_name)
    print(install_path)
    # C:\Program Files\WindowsApps\Microsoft.WindowsCalculator_11.2411.1.0_x64__8wekyb3d8bbwe

    selected_icon = locate_icon(icon_path, install_path)
    print(selected_icon)
    # C:\Program Files\WindowsApps\Microsoft.WindowsCalculator_11.2411.1.0_x64__8wekyb3d8bbwe\Assets\CalculatorStoreLogo.scale-200.png

    show_icon(selected_icon)
    # see the proof


if __name__ == "__main__":
    # Let's use "Microsoft.WindowsCalculator" as example.
    # Names can be listed by `Get-AppxPackage | Select-Object -ExpandProperty Name`
    main("Microsoft.WindowsStore")
