import base64
import json
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import httpretty
import pytest
import time_machine

from snsary.contrib.octopus import OctopusSensor


@pytest.fixture
def sensor():
    return OctopusSensor(
        mpxn="mpan",
        serial_number="serial_number",
        token="token-123",
        fuel_type="electricity",
    )


def test_electricity_from_env(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "OCTOPUS_ELECTRICITY_MPAN": "mpan",
            "OCTOPUS_ELECTRICITY_SERIAL": "serial",
            "OCTOPUS_TOKEN": "token",
        },
    )

    mock_init = mocker.patch.object(
        OctopusSensor, "__init__", return_value=None  # required to mock __init__
    )

    assert isinstance(OctopusSensor.electricity_from_env(), OctopusSensor)

    mock_init.assert_called_with(
        mpxn="mpan",
        serial_number="serial",
        token="token",
        fuel_type="electricity",
    )


def test_gas_from_env(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "OCTOPUS_GAS_MPRN": "mprn",
            "OCTOPUS_GAS_SERIAL": "serial",
            "OCTOPUS_TOKEN": "token",
        },
    )

    mock_init = mocker.patch.object(
        OctopusSensor, "__init__", return_value=None  # required to mock __init__
    )

    assert isinstance(OctopusSensor.gas_from_env(), OctopusSensor)

    mock_init.assert_called_with(
        mpxn="mprn",
        serial_number="serial",
        token="token",
        fuel_type="gas",
    )


@time_machine.travel(
    # temporarily set timezone to Europe/London
    datetime(2022, 4, 5, 15, 32, 23, tzinfo=ZoneInfo("Europe/London")),
    tick=False,
)
@httpretty.activate(allow_net_connect=False)
def test_sample(
    sensor,
):
    url = OctopusSensor.CONSUMPTION_URL.format(
        **{
            "mpxn": "mpan",
            "serial_number": "serial_number",
            "period_from": "2022-04-03T23:00:00Z",
            "fuel_type": "electricity",
        }
    )

    httpretty.register_uri(
        httpretty.GET,
        url,
        match_querystring=True,
        body=json.dumps(
            {
                "results": [
                    {
                        "consumption": 0.076,
                        "interval_start": "2022-04-03T22:00:00Z",
                        "interval_end": "2022-04-03T22:30:00Z",
                    }
                ]
            }
        ),
    )

    now = datetime.now().astimezone()
    readings = list(sensor.sample(now=now))
    assert len(readings) == 1

    assert readings[0].value == 0.076
    assert readings[0].sensor_name == "octopus.electricity"
    assert readings[0].name == "consumption"
    assert datetime.fromtimestamp(readings[0].timestamp).minute == 30

    request = httpretty.last_request()
    auth = base64.b64encode(b"token-123:").decode("utf-8")
    assert request.headers["Authorization"] == f"Basic {auth}"


@httpretty.activate(allow_net_connect=False)
def test_sample_error(
    sensor,
):
    httpretty.register_uri(
        httpretty.GET,
        re.compile(".*"),
        status=500,
    )

    with pytest.raises(Exception) as excinfo:
        now = datetime.now().astimezone()
        list(sensor.sample(now=now))

    assert "500 Server Error" in str(excinfo.value)
