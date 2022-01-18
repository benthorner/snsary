import logging
import sys

logger = logging.getLogger('snsary')


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(levelname)s - [%(threadName)s] %(message)s"
    )
