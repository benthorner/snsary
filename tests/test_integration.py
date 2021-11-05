import logging
from contextlib import contextmanager
from datetime import datetime

from freezegun import freeze_time
from retry import retry as retrier

from snsary import App
from snsary.outputs import MockOutput
from snsary.sensors import MockSensor


@contextmanager
def tmp_app(*, sensors=[], outputs=[]):
    app = App(sensors=sensors, outputs=outputs)
    app.start()
    yield app
    app.stop()


def retry(fn):
    # logger=None stops failure logs causing a false positive
    retrier(tries=5, delay=0.5, logger=None)(fn)()


def test_poller_feed(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(), MockOutput()]

    def first_assertions():
        timestamp = int(datetime.utcnow().timestamp())
        assert f'[{str(sensors[0])}] Collected 1 readings.' in caplog.text
        assert f'[{str(outputs[0])}] Reading: <zero {timestamp} 0>' in caplog.text
        assert f'[{str(outputs[1])}] Reading: <zero {timestamp} 0>' in caplog.text

    def second_assertions():
        timestamp = int(datetime.utcnow().timestamp())
        assert f'[{str(outputs[0])}] Reading: <zero {timestamp} 1>' in caplog.text
        assert f'[{str(outputs[1])}] Reading: <zero {timestamp} 1>' in caplog.text

    with freeze_time() as frozen_time:
        app = App(sensors=sensors, outputs=outputs)
        app.start()

        assert '[MainThread] Started.' in caplog.text
        retry(first_assertions)

        frozen_time.tick()
        retry(second_assertions)

    app.stop()
    assert '[MainThread] Stopping.' in caplog.text

    app.wait()
    assert '[MainThread] Bye.' in caplog.text
    assert 'ERROR' not in caplog.text


def test_failing_sensor(caplog):
    sensors = [MockSensor(fail=True, period_seconds=1)]

    def assertions():
        assert f'[{str(sensors[0])}] problem-1' in caplog.text
        assert f'[{str(sensors[0])}] problem-2' in caplog.text

    with tmp_app(sensors=sensors):
        retry(assertions)


def test_failing_output(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(fail=True)]

    def assertions():
        assert f'[{str(sensors[0])}] Collected 1 readings.' in caplog.text
        assert f'[{str(outputs[0])}] problem-1' in caplog.text
        assert f'[{str(outputs[0])}] problem-2' in caplog.text

    with tmp_app(sensors=sensors, outputs=outputs):
        retry(assertions)


def test_stuck_sensor_sample(caplog):
    sensors = [MockSensor(hang=True)]

    with tmp_app(sensors=sensors):
        pass

    assert f'[MainThread] Failed to stop {str(sensors[0])}.' in caplog.text


def test_stuck_sensor_no_stop(caplog):
    sensors = [MockSensor(stop=False)]

    with tmp_app(sensors=sensors):
        pass

    assert f'[MainThread] Failed to detach {str(sensors[0])}.' in caplog.text


def test_stuck_output_flush(caplog):
    outputs = [MockOutput(hang=True)]

    with tmp_app(outputs=outputs):
        pass

    assert f'[MainThread] Failed to flush {str(outputs[0])}.' in caplog.text
