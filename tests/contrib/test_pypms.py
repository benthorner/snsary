import pms
import pytest
from pms.core import reader

from snsary.contrib.pypms import PyPMSSensor


@pytest.fixture
def mock_sensor(mock_serial):
    mock_serial.stub(
        name="wake",
        receive_bytes=b"BM\xe4\x00\x01\x01t",
        send_bytes=(
            b"BM\x00\x1c"  # expected header
            + b".........................."  # payload (to total 32 bytes)
            + b"\x05W"  # checksum = sum(header) + sum(payload)
        ),
    )

    mock_serial.stub(
        name="passive_mode",
        receive_bytes=b"BM\xe1\x00\x00\x01p",
        send_bytes=(
            b"BM\x00\x04"  # expected header
            + b".."  # payload (to total 8 bytes)
            + b"\x00\xef"  # checksum
        ),
    )

    mock_serial.stub(
        name="passive_read",
        receive_bytes=b"BM\xe2\x00\x00\x01q",
        send_bytes=(
            b"BM\x00\x1c"  # expected header
            + b".........................."  # payload (to total 32 bytes)
            + b"\x05W"  # checksum
        ),
    )

    mock_serial.stub(
        name="sleep",
        receive_bytes=b"BM\xe4\x00\x00\x01s",
        send_bytes=(
            b"BM\x00\x04"  # expected header
            + b".."  # payload (to total 8 bytes)
            + b"\x00\xef"  # checksum
        ),
    )

    return mock_serial


@pytest.fixture
def mock_start(mocker):
    return mocker.patch("snsary.contrib.pypms.PollingSensor.start")


@pytest.fixture
def mock_stop(mocker):
    return mocker.patch("snsary.contrib.pypms.PollingSensor.stop")


@pytest.fixture
def sensor(mock_sensor):
    return PyPMSSensor(
        sensor_name="PMSx003",
        port=mock_sensor.port,
        # timeout should be low to avoid failure tests
        # hanging, high to still allow PTY to work
        timeout=0.01,
    )


@pytest.fixture
def started_sensor(sensor, mock_start):
    sensor.start()
    return sensor


def test_name(sensor):
    assert sensor.name == "PMSx003"


def test_init_sensor_not_found():
    with pytest.raises(Exception) as einfo:
        PyPMSSensor(sensor_name="something", port="any")

    assert "KeyError" in str(einfo)


def test_start(
    mock_sensor,
    sensor,
    mock_start,
):
    sensor.start()
    assert mock_sensor.stubs["wake"].called
    assert mock_sensor.stubs["passive_mode"].called
    mock_start.assert_called_once()


@pytest.mark.parametrize("send_bytes", [b"", b"123"])
def test_start_bad_response(
    mock_sensor,
    sensor,
    send_bytes,
):
    mock_sensor.stub(
        name="passive_mode",
        receive_bytes=b"BM\xe1\x00\x00\x01p",
        send_bytes=send_bytes,
    )

    with pytest.raises(reader.UnableToRead) as einfo:
        sensor.start()

    assert str(einfo.value) == "Sensor failed validation"


def test_stop(
    mock_sensor,
    started_sensor,
    mock_stop,
):
    started_sensor.stop()
    assert mock_sensor.stubs["sleep"].called
    mock_stop.assert_called_once()


def test_stop_bad_response(
    mock_sensor,
    started_sensor,
    mock_stop,
):
    mock_sensor.stub(
        name="sleep",
        receive_bytes=b"BM\xe4\x00\x00\x01s",
        send_bytes=b"123",
    )

    started_sensor.stop()
    assert mock_sensor.stubs["sleep"].called
    mock_stop.assert_called_once()


def test_stop_already_closed(
    sensor,
    caplog,
    mock_stop,
):
    sensor.stop()
    assert "Attempting to use a port that is not open" in caplog.text


def test_sample(
    started_sensor,
):
    readings = started_sensor.sample(timestamp="now", elapsed_seconds=0)
    assert len(readings) == 0  # PMSx003 has 10 second warm up

    readings = started_sensor.sample(timestamp="now", elapsed_seconds=10)
    assert len(readings) == 12

    pm10_reading = next(r for r in readings if r.name == "pm10")
    assert pm10_reading.value == 11822
    assert pm10_reading.timestamp == "now"


def test_sample_bad_response(
    mock_sensor,
    started_sensor,
):
    mock_sensor.stub(
        name="passive_read",
        receive_bytes=b"BM\xe2\x00\x00\x01q",
        send_bytes=b"123",
    )

    with pytest.raises(pms.WrongMessageFormat):
        started_sensor.sample(timestamp="now", elapsed_seconds=30)


def test_sample_already_closed(
    sensor,
    mock_stop,
):
    with pytest.raises(StopIteration):
        sensor.sample(timestamp="now", elapsed_seconds=30)
