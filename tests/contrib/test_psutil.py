from psutil._common import sdiskpart

from snsary.contrib.psutil import PSUtilSensor


def test_sample(mocker):
    mocker.patch(
        "snsary.contrib.psutil.psutil.disk_partitions",
        return_value=[
            sdiskpart(
                device="/dev/sda3",
                mountpoint="/",
                fstype="ext4",
                opts="rw,errors=remount-ro",
                maxfile=255,
                maxpath=4096,
            )
        ],
    )

    sensor = PSUtilSensor(
        functions={"disk_partitions": {}},
    )

    readings = list(
        sorted(
            sensor.sample(timestamp="now"),
            key=lambda r: r.name,
        )
    )

    assert len(readings) == 2
    assert readings[0].name == "disk_partitions-0-maxfile"
    assert readings[0].value == 255
    assert readings[0].sensor_name == "psutil"
    assert readings[0].timestamp == "now"


def test_sample_ignores_unavailable_stats(mocker):
    sensor = PSUtilSensor(functions={"foo": {}})
    readings = list(sensor.sample(timestamp="now"))
    assert len(readings) == 0
