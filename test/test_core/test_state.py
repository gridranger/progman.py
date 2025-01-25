from unittest.mock import Mock, patch

from core import State


class TestState:

    def setup_method(self):
        self.test_object = State()

    def test_groups(self):
        self.test_object.shortcuts = [Mock(tags=["foo"])]
        assert self.test_object.groups["foo"].shortcuts == [self.test_object.shortcuts[0]]
        assert len(self.test_object.groups) == 3

    @patch("core.state.Group.set_geometry")
    def test_add_group(self, set_geometry: Mock):
        mock_group = Mock(is_collapsed=True, size=(1, 2), position=(3, 4))
        mock_group.name = "foo"
        self.test_object.add_group(mock_group)
        assert self.test_object.groups["foo"].is_collapsed
        set_geometry.assert_called_once_with("1x2+3+4")

    def test_add_shortcut(self):
        mock_shortcut = Mock(tags=["foo"])
        self.test_object._groups["foo"] = Mock()
        self.test_object.add_shortcut(mock_shortcut)
        assert self.test_object.shortcuts == [mock_shortcut]
        self.test_object._groups["foo"].append.assert_called_once_with(mock_shortcut)
