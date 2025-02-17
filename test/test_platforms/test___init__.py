import sys
from unittest.mock import patch

from pytest import raises


class TestInit:

    def test_windows(self) -> None:
        with patch("platform.system", return_value="windows"):
            import platforms
            assert platforms.IconLoader
        del sys.modules["platforms"]

    def test_linux(self) -> None:
        with patch("platform.system", return_value="linux"):
            with raises(NotImplementedError):
                import platforms  # noqa: F401
