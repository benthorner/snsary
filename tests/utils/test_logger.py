import logging
import sys

from snsary.utils import configure_logging


def test_configure_logging(mocker):
    mock_config = mocker.patch('logging.basicConfig')
    configure_logging()

    mock_config.assert_called_with(
        stream=sys.stdout,
        level=logging.INFO,
        format=mocker.ANY
    )
