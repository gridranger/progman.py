from core.group import Group


class TestGroup:

    def setup_method(self) -> None:
        self.test_object = Group("test_group")

    def test_set_geometry(self) -> None:
        geometry = "400x300+200+150"
        self.test_object.set_geometry(geometry)
        assert self.test_object.position == (200, 150)
        assert self.test_object.size == (400, 300)
