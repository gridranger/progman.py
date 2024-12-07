from subprocess import Popen
from tkinter import Event, Frame, Label, PhotoImage

from progman.progmanwidget import ProgmanWidget
from progman.shortcut import Shortcut


class IconWidget(Frame, ProgmanWidget):

    def __init__(self, shortcut: Shortcut, *args: any, **kwargs: any) -> None:
        Frame.__init__(self, *args, **kwargs, width=84, height=76, cursor="hand2")
        ProgmanWidget.__init__(self, 'icon')
        self.configure(background=self.theme.background)
        self._shortcut = shortcut
        self._icon: PhotoImage | None = None
        self._icon_label: Label | None = None
        self._text_label: Label | None = None

    @property
    def icon(self) -> PhotoImage:
        if self._icon is None:
            self._icon = PhotoImage(file=self._shortcut.icon_path)
        return self._icon

    def update_theme(self) -> None:
        ProgmanWidget.update_theme(self)
        self.configure(background=self.theme.background)
        self._icon_label.configure(background=self.theme.background)
        self._text_label.configure(background=self.theme.background)

    def render(self) -> None:
        ProgmanWidget.render(self)
        self.grid_propagate(False)
        self._icon_label = Label(self, image=self.icon, justify="center", bg=self.theme.background)
        self._text_label = Label(self, text=self._shortcut.name, wraplength=84, justify="center",
                                 bg=self.theme.background)
        self._icon_label.bind("<Button-1>", self.on_click)
        self._text_label.bind("<Button-1>", self.on_click)
        self._icon_label.grid(row=0, column=0, padx=26, pady=0)
        self._text_label.grid(row=1, column=0, pady=(0, 10), padx=10)

    def rename(self, new_name: str) -> None:
        self._shortcut.name = new_name
        self._text_label.configure(text=new_name)

    def on_click(self, _event: Event | None = None) -> None:
        self.select()
        Popen(self._shortcut.launch_command)
        self.after(100, self.deselect)

    def select(self) -> None:
        self._text_label.config(background=self.theme.background_selected,
                                foreground=self.theme.foreground_selected)

    def deselect(self) -> None:
        self._text_label.config(background=self.theme.background,
                                foreground=self.theme.foreground)


if __name__ == "__main__":
    from tkinter import Tk

    from progman.language import Language
    from progman.shortcut import Shortcut
    from progman.theme import Theme
    t = Tk()
    t.language = Language()
    t.theme = Theme()
    s = Shortcut("C:\\WINDOWS\\system32\\control.exe", "/name", "",
                 r"C:\Users\bardo\repos\progman\src\progman\assets\progman.png", name="Settings")
    i = IconWidget(s, t)
    i.render()
    i.grid(row=0, column=0)
    t.mainloop()
