import sys
from unittest.mock import patch

from pytest import mark, raises


class TestInit:

    @mark.skipif(sys.platform != "win32", reason="Runs only on Windows")
    def test_windows(self) -> None:
        with patch("platform.system", return_value="windows"):
            import platforms
            assert platforms.IconLoader
        del sys.modules["platforms"]

    def test_linux(self) -> None:
        with patch("platform.system", return_value="linux"):
            with raises(NotImplementedError):
                import platforms  # noqa: F401
