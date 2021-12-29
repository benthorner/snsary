from dotenv import load_dotenv

from snsary import system
from snsary.contrib.awair import AwairSensor
from snsary.outputs import MockOutput
from snsary.sources import MultiSource
from snsary.utils import configure_logging

load_dotenv()
configure_logging()

MultiSource(
    # expects:
    #
    #  - AWAIR_TOKEN
    #
    *AwairSensor.discover_from_env()
).subscribe(
    MockOutput()
)

system.start_and_wait()
