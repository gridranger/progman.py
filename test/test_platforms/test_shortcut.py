from progman.shortcut import Shortcut


class TestShortcut:

    def setup_method(self) -> None:
        self.test_object = Shortcut("c:/program folder/app folder/app.exe",
                                    "--foo",
                                    "c:/program folder/app_folder",
                                    "c:/program folder/app folder/abc.ico")

    def test_display_name_from_target(self) -> None:
        assert self.test_object.name == "app"

    def test_display_name_from_link(self) -> None:
        test_object = Shortcut("c:/program folder/app folder/app.exe",
                               "--foo",
                               "c:/program folder/app_folder",
                               "c:/program folder/app folder/abc.ico",
                               link_path="c:/users/my_user/app_data/Microsoft/Windows/Start Menu/Programs/efg.lnk")
        assert test_object.name == "efg"

    def test_display_name_from_name(self) -> None:
        self.test_object.name = "foo"
        assert self.test_object.name == "foo"

    def test___eq__(self) -> None:
        test_object_a = Shortcut("c:/program folder/app folder/app.exe",
                                 "--foo",
                                 "c:/program folder/app_folder",
                                 "c:/program folder/app folder/abc.lnk")
        test_object_b = Shortcut("c:/program folder/app folder/app.exe",
                                 "--bar",
                                 "c:/program folder/app_folder",
                                 "c:/program folder/app folder/abc.lnk")
        test_object_c = Shortcut("c:/program folder/app v2 folder/app.exe",
                                 "--foo",
                                 "c:/program folder/app_folder",
                                 "c:/program folder/app folder/abc.lnk")
        test_object_d = Shortcut("c:/program folder/app folder/app.exe",
                                 "--foo",
                                 "c:/users/me",
                                 "c:/program folder/app folder/abc.lnk")
        assert self.test_object == test_object_a
        assert not self.test_object == test_object_b
        assert not self.test_object == test_object_c
        assert not self.test_object == test_object_d
