import os

import pytest

from snsary.contrib.google import BigQueryOutput, reading_pb2

STREAM_NAME = "projects/test-project/datasets/snsary/tables/readings/streams/_default"


@pytest.fixture
def mock_client(mocker):
    # Integration testing with HTTP stubs isn't possible here, as the BigQuery Storage
    # package uses Cython bindings instead of use Python's native transport libraries,
    # which is what HTTP mocking libraries intercept.
    return mocker.patch("google.cloud.bigquery_storage_v1.BigQueryWriteClient")()


@pytest.fixture
def big_query(mock_client):
    return BigQueryOutput(stream=STREAM_NAME)


def test_from_env(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "GOOGLE_BIGQUERY_STREAM": "stream",
        },
    )

    mock_init = mocker.patch.object(
        BigQueryOutput, "__init__", return_value=None  # required to mock __init__
    )

    assert isinstance(BigQueryOutput.from_env(), BigQueryOutput)

    mock_init.assert_called_with(stream="stream")


def test_publish_batch(
    mocker,
    reading,
    big_query,
    mock_client,
):
    mocker.patch("platform.node", return_value="snsary")

    big_query.publish_batch([reading])
    assert mock_client.append_rows.called

    last_call = mock_client.append_rows.mock_calls[0]
    assert last_call.kwargs["retry"].deadline == big_query.RETRY_DEADLINE

    request = next(last_call.kwargs["requests"])
    assert request.write_stream == STREAM_NAME

    proto_rows = request.proto_rows
    assert proto_rows.writer_schema.proto_descriptor.name == "Reading"

    serialized_rows = proto_rows.rows.serialized_rows
    assert len(serialized_rows) == 1

    proto_reading = reading_pb2.Reading.FromString(serialized_rows[0])
    assert proto_reading.host == "snsary"
    assert proto_reading.sensor == "mysensor"
    assert proto_reading.metric == "myreading"
    assert proto_reading.timestamp == "2022-04-23T20:25:46+00:00"
    assert proto_reading.value == 123


def test_publish_batch_error(
    big_query,
    mock_client,
):
    mock_client.append_rows.side_effect = TypeError

    with pytest.raises(Exception):
        big_query.publish_batch([])
