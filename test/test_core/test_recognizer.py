from unittest.mock import Mock

from core import Recognizer


class TestRecognizer:

    def setup_method(self) -> None:
        self.test_object = Recognizer()

    def test_negative_name_hint(self) -> None:
        shortcut = Mock(tags=[])
        shortcut.name = "Node.js"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_negative_extension_hint(self) -> None:
        shortcut = Mock(target_path=r"c:\users\my_user\desktop\some.url", tags=[])
        shortcut.name = "Some URL"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_negative_path_hint(self) -> None:
        shortcut = Mock(target_path=r"c:\program files\thrid party app\Uninstaller.exe", tags=[])
        shortcut.name = "Remove Third Party App"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Hidden"]

    def test_path_hint(self) -> None:
        shortcut = Mock(target_path=r"c:\program files\steam\steamapps\common\skyrim\bin\skyrim.exe", tags=[])
        shortcut.name = "Skyrim"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Games"]

    def test_name_hint(self) -> None:
        shortcut = Mock(target_path="foo", tags=[])
        shortcut.name = "VSCode"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Development"]

    def test_no_hints(self) -> None:
        shortcut = Mock(target_path="c:/my/app.exe", tags=[])
        shortcut.name = "My App"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["New"]

    def test_already_tagged(self) -> None:
        original_tags = ["Development", "Accessories"]
        shortcut = Mock(target_path="c:/my/app.exe", tags=original_tags)
        shortcut.name = "My App"
        self.test_object.categorize(shortcut)
        assert shortcut.tags == ["Development", "Accessories"]
