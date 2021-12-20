from snsary import system
from snsary.contrib.pypms import PyPMSSensor
from snsary.outputs import MockOutput
from snsary.utils import configure_logging

PyPMSSensor(sensor_name='PMSx003').subscribe(MockOutput())
configure_logging()
system.start_and_wait()
