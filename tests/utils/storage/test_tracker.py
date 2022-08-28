import pytest

from snsary.utils.storage.tracker import Tracker
from tests.conftest import create_reading


@pytest.fixture
def tracker():
    class FakeTracker(Tracker):
        def __init__(self):
            Tracker.__init__(self, "FakeTracker", foo=max, bar=min)

        def on_change(self, old, new):
            self.changed_old = old
            self.changed_new = new

    return FakeTracker()


def test_update(tracker, mock_store):
    readings = [
        create_reading(name="foo", value=1),
        create_reading(name="bar", value=2),
        create_reading(name="other"),
    ]

    old_values = {"foo": 0, "bar": 1}
    mock_store["FakeTracker-tracked-values"] = old_values

    tracker.update(readings)
    assert tracker.changed_old == old_values

    expected_values = {"foo": 1, "bar": 1}
    assert mock_store["FakeTracker-tracked-values"] == expected_values
    assert tracker.changed_new == expected_values


def test_update_no_store(tracker, mock_store):
    readings = [
        create_reading(name="foo", value=1),
        create_reading(name="bar", value=2),
    ]

    tracker.update(readings)
    assert tracker.changed_old == {}

    expected_values = {"foo": 1, "bar": 2}
    assert mock_store["FakeTracker-tracked-values"] == expected_values
    assert tracker.changed_new == expected_values


@pytest.mark.parametrize(
    "readings",
    [
        [create_reading(name="foo")],
        [create_reading(name="foo", value=1), create_reading(name="bar", value=2)],
    ],
)
def test_update_no_change(tracker, mock_store, readings):
    expected_values = {"foo": 1, "bar": 2}
    mock_store["FakeTracker-tracked-values"] = expected_values

    tracker.update(readings)
    assert "changed_new" not in dir(tracker)
    assert mock_store["FakeTracker-tracked-values"] == expected_values
