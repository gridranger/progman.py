from .icon import IconWidget
from .progmanwidgets import ProgmanWidget
from .scrollframe import ScrollFrame


class IconDrawer(ScrollFrame, ProgmanWidget):

    def __init__(self, *args, **kwargs):
        ScrollFrame.__init__(self, *args, **kwargs)
        ProgmanWidget.__init__(self, "icon_drawer")
        self._icons: list[IconWidget]  = []
        self.viewPort.on_enter = self.on_enter
        self.viewPort.on_leave = self.on_leave

    def update_theme(self) -> None:
        self.configure(bg=self.theme.background)
        ProgmanWidget.update_theme(self)

    def render(self) -> None:
        for shortcut in self.state.shortcuts:
            if "Development" in shortcut.tags:
                self._icons.append(IconWidget(shortcut, self.viewPort))
        self.grid(row=0, column=0, sticky="nesw")
        ProgmanWidget.render(self)
        self.update_theme()
        self._arrange_icons()

    def _arrange_icons(self):
        max_columns = self.master.winfo_width() // IconWidget.WIDTH
        for index, icon in enumerate(self._icons):
            row = index // max_columns
            column = index % max_columns
            icon.grid(row=row, column=column)

    def update_size(self, width: int, height: int) -> None:
        self.configure(width=width, height=height)
        self.viewPort.configure(width=width, height=height)
        self._arrange_icons()
        self._update_scrollbar()

    def _update_scrollbar(self) -> None:
        last_icon = list(self.viewPort.children.values())[-1]
        if last_icon.winfo_y() > self.winfo_height():
            self._place_scrollbar()
        else:
            self.vsb.grid_forget()
