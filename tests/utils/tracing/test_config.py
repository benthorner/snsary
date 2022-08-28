import pytest

from snsary.utils.tracing.config import Config


def test_get_set():
    config = Config()

    # "*" matches at any level
    config.set("*.attr", 1)
    assert config.get("p1.attr") == 1
    assert config.get("p1.p2.attr") == 1
    assert config.get("p1.p2.p3.attr") == 1

    # prioritise specific patterns
    config.set("p1.attr", 2)
    assert config.get("p1.attr") == 2
    assert config.get("p1.p2.attr") == 1
    assert config.get("p1.p2.p3.attr") == 1

    # prioritise longer patterns
    config.set("p1.*.attr", 3)
    assert config.get("p1.attr") == 2
    assert config.get("p1.p2.attr") == 3
    assert config.get("p1.p2.p3.attr") == 3

    # ignore less specific pattern
    config.set("*.*.attr", 4)
    assert config.get("p1.p2.attr") == 3
    assert config.get("p1.p2.p3.attr") == 3

    # prioritise more specific pattern
    config.set("p1.p2.attr", 4)
    assert config.get("p1.p2.attr") == 4
    assert config.get("p1.p2.p3.attr") == 3

    # prioritise even longer pattern
    config.set("*.*.*.attr", 5)
    assert config.get("p1.p2.p3.attr") == 5

    # return default if no match found
    assert config.get("unknown", default=[]) == []

    # raise error if no default provided
    with pytest.raises(KeyError):
        config.get("something.else")


def test_reset():
    config = Config()
    config.set("a", "c")
    assert config.get("a") == "c"

    config.reset()
    with pytest.raises(KeyError):
        config.get("a")
