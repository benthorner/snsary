from dotenv import load_dotenv

from snsary import system
from snsary.contrib.octopus import OctopusSensor
from snsary.outputs import MockOutput
from snsary.utils import configure_logging

load_dotenv()
configure_logging()

# expects:
#
#  - OCTOPUS_MPAN
#  - OCTOPUS_SERIAL
#  - OCTOPUS_TOKEN
#
OctopusSensor.from_env().subscribe(MockOutput())
system.start_and_wait()
