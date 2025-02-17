from unittest.mock import Mock, patch

from core import Shortcut


class TestShortcut:
    namespace = "core.shortcut"

    def setup_method(self):
        self.test_object = Shortcut(
            target_path="/usr/bin/app",
            arguments="--arg1 value1",
            workdir_path="/home/my_user/documents",
            separate_icon_path="/home/my_user/images/app_icon.png"
        )

    def test_display_name_from_link(self) -> None:
        test_object = Shortcut("c:/program folder/app folder/app.exe",
                               "--foo",
                               "c:/program folder/app_folder",
                               "c:/program folder/app folder/abc.ico",
                               link_path="c:/users/my_user/app_data/Microsoft/Windows/Start Menu/Programs/efg.lnk")
        assert test_object.name == "efg"

    @patch(f"{namespace}.Path.exists", return_value=True)
    def test_icon(self, exists: Mock):
        assert self.test_object.icon == self.test_object.separate_icon_path
        exists.assert_called_once()

    def test_icon_protected_by_windows(self):
        self.test_object.separate_icon_path = r"c:\windows\installer\{ugly-hash}\foo.ico"
        self.test_object.icon_index = 9
        assert self.test_object.icon == self.test_object.target_path
        assert self.test_object.icon_index == 0

    def test_launch_command(self):
        assert self.test_object.launch_command == ["/usr/bin/app", "--arg1", "value1"]

    def test___eq__(self):
        other = Mock(
            target_path="/usr/bin/app",
            arguments="--arg1 value1",
            workdir_path="/home/my_user/Documents",
            separate_icon_path="/home/my_user/images/app_icon.png"
        )
        with patch(f"{self.namespace}.name", "linux"):
            assert self.test_object != other
        with patch(f"{self.namespace}.name", "nt"):
            assert self.test_object == other

    def test___hash__(self):
        with patch("builtins.hash") as mocked_hash:
            result = self.test_object.__hash__()
        assert result == mocked_hash.return_value
        mocked_hash.assert_called_once_with("/usr/bin/app--arg1 value1/home/my_user/documents")

    def test_is_web_link(self):
        assert self.test_object.is_web_link is False
        self.test_object.target_path = "https://google.com"
        assert self.test_object.is_web_link
