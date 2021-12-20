from snsary.sources import MultiSource


def test_subscribe(mocker):
    source = MultiSource()
    mock_stream = mocker.patch.object(source.stream, 'subscribe')
    source.subscribe('output')
    mock_stream.assert_called_with('output')
