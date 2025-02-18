from tkinter import Event, Menu, Misc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import MenuItem


class ContextMenu:

    def __init__(self) -> None:
        self._menu_items: list[MenuItem] = []
        self._context_menu: Menu | None = None
        self._sub_menus: dict[str, Menu] = {}

    def render_context_menu(self) -> None:
        if self._context_menu:
            self._context_menu.destroy()
        self._context_menu = Menu(self, tearoff=0)
        for item in self._menu_items:
            if item.type == "separator":
                self._context_menu.add_separator()
            elif item.type == "submenu":
                self._sub_menus[item.label] = Menu(self._context_menu, tearoff=0)
                self._context_menu.add_cascade(label=self.get_label(item.label), menu=self._sub_menus[item.label])
            else:
                self._context_menu.add_command(label=self.get_label(item.label), command=item.command, state=item.state)

    def bind_context_menu_to(self, items_to_bind_to: list[Misc]) -> None:
        for item in items_to_bind_to:
            item.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event: Event) -> None:
        self._context_menu.post(event.x_root, event.y_root)
