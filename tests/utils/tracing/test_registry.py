from threading import Thread

import pytest

from snsary.utils.tracing import Config, Monitor, Registry


@pytest.fixture
def config():
    return Config()


class FakeMonitor(Monitor):
    pass


def test_get(config):
    config.set("some.id.monitors", [FakeMonitor.factory()])
    registry = Registry(config)
    monitors = registry.get("some.id")

    assert len(monitors) == 1
    assert isinstance(monitors[0], FakeMonitor)

    assert registry.get("some.id") == monitors
    assert registry.get("other.id") != monitors


def test_get_no_config():
    registry = Registry(Config())
    assert len(registry.get("some.id")) == 0


def test_get_thread_aware(config):
    config.set("thread_aware", True)
    config.set("monitors", [FakeMonitor.factory()])
    registry = Registry(config)
    monitors = registry.get("some.id")
    other_monitors = None

    def target():
        nonlocal other_monitors
        other_monitors = registry.get("some.id")

    thread = Thread(target=target)
    thread.start()
    thread.join()

    assert monitors != other_monitors
    assert len(other_monitors) == 1
    assert isinstance(other_monitors[0], FakeMonitor)


def test_get_not_thread_aware(config):
    config.set("monitors", [FakeMonitor.factory()])
    registry = Registry(config)
    monitors = registry.get("some.id")
    other_monitors = None

    def target():
        nonlocal other_monitors
        other_monitors = registry.get("some.id")

    thread = Thread(target=target)
    thread.start()
    thread.join()

    assert monitors == other_monitors
