from functools import partial
from tkinter import TclError
from unittest.mock import patch, Mock

from core import Shortcut
from programmanager import ProgramManager
from ui.mainwindow import MainWindow


class TestSample:
    namespace = "ui.mainwindow"

    # def test_suite(self):
    #     self.app = ProgramManager()
    #
    #     def hook(self, test_class):
    #         test_cases = [method for method in dir(test_class) if method.startswith("tkinter_test_")]
    #         for test_case in test_cases:
    #             getattr(test_class, test_case)(self)
    #         self.destroy()
    #
    #     self.app._root._run_test_hook = partial(hook, self.app._root, self)
    #     try:
    #         self.app.run()
    #     except TclError as e:
    #         if "application has been destroyed" not in str(e):
    #             raise e from None  # pragma: no cover
    #
    # def tkinter_test_create_new_icon_in_closed_group(self, main_window: MainWindow):
    #     with patch("ui.mainwindow.IconPropertiesDialog)") as mock_dialog, \
    #             patch.object(main_window.app_state, "add_shortcut") as mock_add_shortcut:
    #         mock_dialog.result = Shortcut("c:/myapp/myapp.exe", "/arg1 /arg2", "c:/myapp/", "c:/myapp.ico", 0, "MyApp",
    #                                       tags=["Accessories"])
    #         main_window._menubar.winfo_children()[0].invoke(1)
    #     mock_dialog.assert_called_once_with(main_window, "new_icon")
    #     mock_add_shortcut.assert_called_once_with(mock_dialog.result)
