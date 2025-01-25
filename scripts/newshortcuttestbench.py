from tkinter import Tk

from core import State
from ui.iconpropertiesdialog import IconPropertiesDialog


class App(Tk):
    def __init__(self):
        super().__init__()
        self.app_state = State()
        self.title("New Shortcut Test Bench")
        new_shortcut = IconPropertiesDialog(self, "new_icon")
        print(new_shortcut.result)


if __name__ == "__main__":
    app = App().mainloop()
