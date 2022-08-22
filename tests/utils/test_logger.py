import logging
import sys
from threading import Thread

from snsary.utils import HasLogger, configure_logging, get_logger
from tests.conftest import retry


def test_HasLogger_name():
    assert HasLogger().name == "HasLogger"


def test_HasLogger_logger():
    assert HasLogger().logger.name == "snsary.haslogger"


def test_get_logger_main_thread():
    assert get_logger().name == "snsary"


def test_get_logger_not_found(mocker):
    mock_thread = mocker.patch("snsary.utils.logger.current_thread")
    mock_thread().ident = "rand"  # mock ident to avoid reuse issues
    assert get_logger().name == "snsary.anon-rand"


def test_get_logger_child_thread(caplog):
    caplog.set_level(logging.INFO)

    def in_a_thread():
        get_logger("foo").warning("testing")
        get_logger().info("success")

    def assertions():
        assert "WARNING - [snsary.foo] testing" in caplog.text
        assert "INFO - [snsary.foo] success" in caplog.text

    thread = Thread(target=in_a_thread)
    thread.start()

    thread.join()
    retry(assertions)


def test_configure_logging(mocker):
    mock_config = mocker.patch("logging.basicConfig")
    configure_logging()

    mock_config.assert_called_with(
        stream=sys.stdout, level=logging.INFO, format=mocker.ANY
    )
