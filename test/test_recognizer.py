from unittest.mock import Mock

from progman.core import Recognizer


class TestRecognizer:

    def setup_method(self):
        self.test_object = Recognizer()

    def test_negative_name_hint(self):
        shortcut = Mock()
        shortcut.name = "Node.js"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_negative_extension_hint(self):
        shortcut = Mock(target_path=r"c:\users\my_user\desktop\some.url")
        shortcut.name = "Some URL"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_negative_path_hint(self):
        shortcut = Mock(target_path=r"c:\program files\thrid party app\Uninstaller.exe")
        shortcut.name = "Remove Third Party App"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_path_hint(self):
        shortcut = Mock(target_path=r"c:\program files\steam\steamapps\common\skyrim\bin\skyrim.exe")
        shortcut.name = "Skyrim"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Games"]

    def test_name_hint(self):
        shortcut = Mock(target_path="foo")
        shortcut.name = "VSCode"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Development"]

    def test_no_hints(self):
        shortcut = Mock(target_path="c:/my/app.exe")
        shortcut.name = "My App"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["New"]
