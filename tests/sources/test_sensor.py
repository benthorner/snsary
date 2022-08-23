def test_subscribe(mocker, sensor):
    mock_stream = mocker.patch.object(sensor.stream, "subscribe")
    sensor.subscribe("output")
    mock_stream.assert_called_with("output")
