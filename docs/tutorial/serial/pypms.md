# PyPMS

_This guide is written for the [PMSA003 Air Monitoring HAT for Raspberry Pi](https://thepihut.com/products/air-monitoring-hat-for-raspberry-pi-pmsa003) and assumes you've already connected it to your Pi. It only covers the PMS, not the OLED display._

## Prepare to monitor the PMS

Snsary has an adapter ([`contrib/pypms.py`](../../../src/snsary/contrib/pypms.py)) for [the excellent PyPMS library](https://github.com/avaldebe/PyPMS), which knows how to configure and read from the PMSA003 and lots of other PMSs. It also has a built in CLI.

Install the PyPMS library / CLI to test the PMS works.

```bash
# you can install it standalone
pip3 install pypms

# or as an extra for snsary
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[pypms]

# test the sensor works
pms --debug -m PMSx003 -s /dev/ttyS0 -i 5 serial
```

You should eventually see a line that looks like this:

> 2021-11-26 23:40:31: PM1 1.0, PM2.5 8.0, PM10 8.0 μg/m3

It's worth noting the `DEBUG` output: it takes several seconds for the device to respond to the `wake` command; the device also returns a lot of garbage output initially, before valid readings come through.

## Add PyPMSSensor to your app

See [examples/serial/pypms.py](../../examples/serial/pypms.py).

You should see something like the following at startup:

```
2021-12-12 11:34:59,401 - INFO - [pmsx003-1968873328] Still warming up, no data yet.
2021-12-12 11:34:59,401 - INFO - [pmsx003-1968873328] Collected 0 readings.
2021-12-12 11:35:04,402 - INFO - [pmsx003-1968873328] Still warming up, no data yet.
2021-12-12 11:35:04,403 - INFO - [pmsx003-1968873328] Collected 0 readings.
2021-12-12 11:35:09,446 - INFO - [pmsx003-1968873328] Collected 12 readings.
```

The "warm up" is necessary as the first two samples always [raise an InconsistentObservation exception](https://github.com/avaldebe/PyPMS/blob/04ff8edede7d780018cd00a7fcf78ffed43c0de4/src/pms/sensors/plantower/pmsx003.py#L63). The fault is probably the library not following the device protocol, but it only affects the first two readings.

_Note: Adafruit have a UART driver for PMSs, but [it doesn't seem to work for the one covered in this article](https://github.com/adafruit/Adafruit_CircuitPython_PM25/issues/9). PyPMS is more thoroughly tested and offers significant compatibility with a range of PMS devices._
