import pytest

from snsary.utils.tracing import Monitor, Sample, capture_exceptions, configure, reset


@pytest.fixture
def fake_monitor():
    class FakeMonitor(Monitor):
        samples = []

        def analyse(self, sample):
            FakeMonitor.samples += [sample]

    return FakeMonitor


@pytest.fixture(autouse=True)
def tracing_session():
    yield
    reset()


@capture_exceptions("failure")
def wrapped_failure():
    raise Exception("uh oh")


@capture_exceptions("success")
def wrapped_success():
    return "pass"


def test_capture_exceptions(
    fake_monitor,
    caplog,
):
    configure(
        {
            "*.enabled": True,
            "*.monitors": [fake_monitor.factory()],
        }
    )

    assert not wrapped_failure()
    assert wrapped_success() == "pass"

    assert fake_monitor.samples == [Sample.FAILURE, Sample.SUCCESS]
    assert "uh oh" in caplog.text


def test_capture_exceptions_without_tracing(
    fake_monitor,
):
    with pytest.raises(Exception):
        wrapped_failure()

    assert wrapped_success() == "pass"
    assert len(fake_monitor.samples) == 0


def test_capture_exceptions_partial_tracing(
    fake_monitor,
):
    configure(
        {
            "success.monitors": [fake_monitor.factory()],
            "success.enabled": True,
        },
    )
    assert wrapped_success() == "pass"
    assert len(fake_monitor.samples) == 1

    configure({"success.enabled": False})
    assert wrapped_success() == "pass"
    assert len(fake_monitor.samples) == 1


def test_capture_exceptions_persists_monitors(
    fake_monitor,
):
    configure(
        {
            "success.monitors": [fake_monitor.factory()],
            "success.enabled": True,
        }
    )

    wrapped_success()
    assert len(fake_monitor.samples) == 1

    configure({"success.monitors": ["not a monitor"]})
    wrapped_success()
    assert len(fake_monitor.samples) == 2
