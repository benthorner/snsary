import pytest

from snsary.utils.tracing.config import Config


def test_get_set():
    config = Config()

    # exact match
    config.set("prefix.attr", 1)
    assert config.get("prefix.attr") == 1

    # no match
    with pytest.raises(KeyError):
        config.get("prefix.more.attr")

    # default match
    assert config.get("prefix.more.attr", default=1) == 1
    assert config.get("prefix.attr", default=2) == 1

    # top-level match
    config.set("attr", 2)
    assert config.get("prefix.more.attr") == 2
    assert config.get("prefix.attr") == 1


def test_reset():
    config = Config()
    config.set("attr", 1)
    assert config.get("prefix.attr") == 1

    config.reset()
    with pytest.raises(KeyError):
        config.get("prefix.attr")
