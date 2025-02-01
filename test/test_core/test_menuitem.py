from core import MenuItem


class TestMenuItem:

    def test___post_init__(self):
        assert MenuItem("foo").type == "command"
        assert MenuItem("separator").type == "separator"
