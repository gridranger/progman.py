from abc import ABC, abstractmethod
from tkinter import Event, Frame, Label, PhotoImage

from ui.progmanwidgets import ProgmanWidget


class Icon(ABC, Frame, ProgmanWidget):
    WIDTH = 84
    HEIGHT = 76

    def __init__(self, *args: any, **kwargs: any) -> None:
        Frame.__init__(self, *args, **kwargs, width=self.WIDTH, height=self.HEIGHT)
        ProgmanWidget.__init__(self, 'icon')
        self.configure(background=self.theme.background)
        self._icon = None
        self._icon_label: Label | None = None
        self._text_label: Label | None = None

    @property
    @abstractmethod
    def icon(self) -> PhotoImage:
        pass

    @property
    @abstractmethod
    def _label(self) -> str:
        pass

    @abstractmethod
    def _launch(self) -> None:
        pass

    def update_theme(self) -> None:
        ProgmanWidget.update_theme(self)
        self.configure(background="self.theme.background")
        self._icon_label.configure(background=self.theme.background)
        self._text_label.configure(background=self.theme.background)

    def render(self) -> None:
        ProgmanWidget.render(self)
        self.grid_propagate(False)
        self._icon_label = Label(self, image=self.icon, justify="center", bg=self.theme.background, cursor="hand2")
        self._text_label = Label(self, text=self._label, wraplength=74, justify="center", bg=self.theme.background, cursor="hand2")
        self._icon_label.bind("<Button-1>", self.on_click)
        self._text_label.bind("<Button-1>", self.on_click)
        self._icon_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=26, pady=0)
        self._text_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=5, pady=0)
        for widget in [self, self._icon_label, self._text_label]:
            widget.bind("<Enter>", self.master.on_enter)
            widget.bind("<Leave>", self.master.on_leave)

    def on_click(self, _event: Event | None = None) -> None:
        self.select()
        self._launch()
        self.after(100, self.deselect)

    def select(self) -> None:
        self._text_label.config(background=self.theme.background_selected,
                                foreground=self.theme.foreground_selected)

    def deselect(self) -> None:
        self._text_label.config(background=self.theme.background,
                                foreground=self.theme.foreground)
