from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from snsary.outputs import BatchOutput


@pytest.fixture()
def output():
    class Output(BatchOutput):
        def publish_batch(self, readings):
            pass

    return Output()


@pytest.fixture()
def mock_publish_batch(output, mocker):
    return mocker.patch.object(output, 'publish_batch')


def test_stop(
    output,
    mock_publish_batch,
):
    output.stop()
    mock_publish_batch.assert_not_called()

    output.publish('reading')
    mock_publish_batch.assert_not_called()

    output.stop()
    mock_publish_batch.assert_called_with(['reading'])


def test_publish_forwards_large_batches(
    output,
    mock_publish_batch
):
    for _ in range(1, 101):
        output.publish('reading')

    mock_publish_batch.assert_called_with(['reading'] * 100)


def test_publish_forwards_old_batches(
    output,
    mock_publish_batch,
):
    output.publish('reading')

    with freeze_time(datetime.now() + timedelta(seconds=10)):
        output.publish('reading')

    mock_publish_batch.assert_called_with(['reading'] * 2)
