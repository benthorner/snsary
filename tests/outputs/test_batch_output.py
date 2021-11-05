from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from snsary.outputs import BatchOutput


@pytest.fixture()
def output():
    class Output(BatchOutput):
        def send_batch(self, readings):
            pass

    return Output()


@pytest.fixture()
def mock_send_batch(output, mocker):
    return mocker.patch.object(output, 'send_batch')


def test_send_forwards_large_batches(
    output,
    mock_send_batch
):
    for _ in range(1, 101):
        output.send('reading')

    mock_send_batch.assert_called_with(['reading'] * 100)


def test_send_forwards_old_batches(
    output,
    mock_send_batch,
):
    output.send('reading')

    with freeze_time(datetime.now() + timedelta(seconds=10)):
        output.send('reading')

    mock_send_batch.assert_called_with(['reading'] * 2)
