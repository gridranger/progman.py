from unittest.mock import Mock, patch

from programmanager import ProgramManager


class TestProgramManager:
    namespace = "programmanager"

    def setup_method(self):
        self.test_object = ProgramManager()

    def test_run(self):
        self.test_object._load_os_content = Mock()
        self.test_object._root = Mock()
        self.test_object.run()
        self.test_object._load_os_content.assert_called_once()
        self.test_object._root.render.assert_called_once()
        self.test_object._root.protocol.assert_called_once_with("WM_DELETE_WINDOW", self.test_object._root.save_on_quit)
        self.test_object._root.mainloop.assert_called_once()

    @patch(f"{namespace}.ShortcutCollector.collect_links", return_value=[Mock()])
    @patch(f"{namespace}.Recognizer.categorize")
    def test__load_os_content(self, categorize: Mock, collect_links: Mock):
        self.test_object.app_state = Mock(shortcuts=[])
        self.test_object._load_os_content()
        assert self.test_object.app_state.shortcuts == collect_links.return_value
        categorize.assert_called_once_with(self.test_object.app_state.shortcuts[0])
