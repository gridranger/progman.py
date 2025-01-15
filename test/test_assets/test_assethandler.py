from unittest.mock import Mock, patch

from assets import asset_storage
from assets.assethandler import AssetHandler


class TestAssetHandler:
    namespace = "assets.assethandler"

    def setup_method(self):
        self.test_object = AssetHandler()

    def test_module_level__init__(self):
        assert isinstance(asset_storage, AssetHandler)

    def test___init__(self):
        assert self.test_object._available_images

    def test___getitem___content_exist(self):
        self.test_object._content["blank"] = Mock()
        assert self.test_object["blank"] == self.test_object._content["blank"]

    @patch(f"{namespace}.PhotoImage")
    @patch(f"{namespace}.Path", return_value=Mock(stem="new"))
    def test___getitem___content_not_exist(self, path: Mock, photo_image: Mock):
        self.test_object._available_images = ["new.png"]
        assert self.test_object["new"] == photo_image.return_value
        photo_image.assert_called_once_with(file="new.png")
        path.assert_called_once_with("new.png")

    @patch(f"{namespace}.PhotoImage")
    @patch(f"{namespace}.Path", return_value=Mock(stem="new"))
    def test___getitem___plank_placholder_returned(self, path: Mock, photo_image: Mock):
        self.test_object._content["blank"] = Mock()
        self.test_object._available_images = []
        assert self.test_object["new"] == self.test_object._content["blank"]

    def test_get_ion(self):
        self.test_object._content["my_file-0"] = Mock()
        assert self.test_object.get_icon("my_file", 0) == self.test_object._content["my_file-0"]

    def test_store_icon(self):
        image = Mock()
        self.test_object.store_icon("my_file", 0, image)
        assert self.test_object._content["my_file-0"] == image
