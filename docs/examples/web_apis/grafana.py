from dotenv import load_dotenv

from snsary import system
from snsary.contrib.grafana import GraphiteOutput
from snsary.sources import MockSensor
from snsary.utils import configure_logging

load_dotenv()
configure_logging()

MockSensor().subscribe(
    # expects:
    #
    #  - GRAPHITE_URL
    #
    GraphiteOutput.from_env()
)

system.start_and_wait()
