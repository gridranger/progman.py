from unittest.mock import Mock

from core.group import Group


class TestGroup:

    def setup_method(self) -> None:
        self.test_object = Group("test_group")

    def test_set_geometry(self) -> None:
        geometry = "400x300+200+150"
        test_object = Group("test_group", geometry=geometry)
        assert test_object.position == (200, 150)
        assert test_object.size == (400, 300)

    def test_is_empty(self) -> None:
        assert self.test_object.is_empty
        self.test_object.shortcuts.append(Mock())
        assert not self.test_object.is_empty

    def test_append(self) -> None:
        mock_shortcut = Mock()
        self.test_object.append(mock_shortcut)
        assert self.test_object.shortcuts == [mock_shortcut]
