# Origin: https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
# But was updated heavily by me.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from platform import system
from tkinter import Event, Scrollbar, Tk

from ui.progmanwidgets import ProgmanCanvas, ProgmanFrame


# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(ProgmanFrame):

    def __init__(self, parent: Tk, *args: any, **kwargs: any) -> None:
        ProgmanFrame.__init__(self, parent, *args, **kwargs)  # create a frame (self)
        self.canvas = ProgmanCanvas(self, borderwidth=0, background="#ffffff")  # place canvas on self
        self.viewPort = ProgmanFrame(self.canvas, background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = Scrollbar(parent, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas
        self._place_scrollbar()  # pack scrollbar to right of self
        self.canvas.grid(row=0, column=0, sticky="nsew")  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort")  # add view port frame to canvas
        self.viewPort.bind("<Configure>", self._on_frame_configure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self._on_canvas_configure)  # bind an event whenever the size of the canvas frame changes.
        self.viewPort.bind('<Enter>', self.on_enter)  # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.on_leave)  # unbind wheel events when the cursor leaves the control
        self._on_frame_configure(None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def _place_scrollbar(self) -> None:
        self.vsb.grid(row=0, column=1, sticky="ns")

    def _on_frame_configure(self, _event: Event | None) -> None:
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(width=self.master.winfo_width(), height=self.master.winfo_height())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def _on_canvas_configure(self, event: Event) -> None:
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

    def _on_mouse_wheel(self, event: Event) -> None:  # cross-platform scroll wheel event
        if system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def on_enter(self, _event: Event) -> None:  # bind wheel events when the cursor enters the control
        if system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def on_leave(self, _event: Event) -> None:  # unbind wheel events when the cursor leaves the control
        if system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
