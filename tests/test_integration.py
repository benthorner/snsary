import logging
from contextlib import contextmanager
from datetime import datetime
from threading import Thread

from freezegun import freeze_time
from retry import retry as retrier

from snsary import system
from snsary.outputs import MockOutput
from snsary.sources import MockSensor, MultiSource
from snsary.utils import Service


@contextmanager
def tmp_app(*, sensors=[], outputs=[]):
    try:
        MultiSource(*sensors).stream.into(*outputs)
        system.start()
        yield
        system.stop()
    finally:
        Service.clear()


def retry(fn):
    # logger=None stops failure logs causing a false positive
    retrier(tries=5, delay=0.5, logger=None)(fn)()


def test_system(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(), MockOutput()]

    def first_assertions():
        timestamp = int(datetime.utcnow().timestamp())
        assert 'INFO - [MainThread] Started.' in caplog.text
        assert f'INFO - [{str(sensors[0])}] Collected 1 readings.' in caplog.text
        assert f'INFO - [{str(outputs[0])}] Reading: <zero {timestamp} 0>' in caplog.text
        assert f'INFO - [{str(outputs[1])}] Reading: <zero {timestamp} 0>' in caplog.text

    def second_assertions():
        timestamp = int(datetime.utcnow().timestamp())
        assert f'INFO - [{str(outputs[0])}] Reading: <zero {timestamp} 1>' in caplog.text
        assert f'INFO - [{str(outputs[1])}] Reading: <zero {timestamp} 1>' in caplog.text

    def end_assertions():
        assert 'INFO - [MainThread] Stopping.' in caplog.text
        assert 'INFO - [MainThread] Bye.' in caplog.text
        assert 'ERROR' not in caplog.text

    with freeze_time() as frozen_time:
        with tmp_app(sensors=sensors, outputs=outputs):
            retry(first_assertions)
            frozen_time.tick()
            retry(second_assertions)

    retry(end_assertions)


def test_failing_sensor(caplog):
    sensors = [MockSensor(fail=True, period_seconds=1)]

    def assertions():
        assert f'ERROR - [{str(sensors[0])}] problem-1' in caplog.text
        assert f'ERROR - [{str(sensors[0])}] problem-2' in caplog.text

    with tmp_app(sensors=sensors):
        retry(assertions)


def test_failing_output(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(fail=True)]

    def assertions():
        assert f'INFO - [{str(sensors[0])}] Collected 1 readings.' in caplog.text
        assert f'ERROR - [{str(outputs[0])}] problem-1' in caplog.text
        assert f'ERROR - [{str(outputs[0])}] problem-2' in caplog.text

    with tmp_app(sensors=sensors, outputs=outputs):
        retry(assertions)


def test_stuck_sensor_service(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(hang=True), MockSensor()]

    def assertions():
        assert f'INFO - [{str(sensors[1])}] Collected 1 readings.' in caplog.text
        assert f'INFO - [{str(sensors[0])}] Collected 1 readings.' not in caplog.text

    with tmp_app(sensors=sensors):
        retry(assertions)

    def end_assertions():
        assert f'ERROR - [MainThread] Failed to stop {str(sensors[0])}.' in caplog.text

    retry(end_assertions)


def test_stuck_output_async(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor()]
    outputs = [MockOutput(hang=True), MockOutput()]

    def assertions():
        assert f'INFO - [{str(outputs[1])}] Reading' in caplog.text
        assert f'INFO - [{str(outputs[0])}] Reading' not in caplog.text

    with tmp_app(sensors=sensors, outputs=outputs):
        retry(assertions)

    def end_assertions():
        assert 'Bye.' in caplog.text
        assert 'ERROR' not in caplog.text

    retry(end_assertions)


def test_wait_stop():
    thread = Thread(
        target=lambda: system.wait(handle_signals=False),
        daemon=True
    )

    thread.start()
    thread.join(timeout=0.1)
    assert thread.is_alive()

    system.stop()
    thread.join(timeout=0.1)
    assert not thread.is_alive()
