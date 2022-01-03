## Serial

Raspberry Pi exposes GPIO 14+15 as a serial device.

_Note: "serial" is ambiguous. It can refer to e.g. UART, I2C, SPI, USB, etc. Here it refers to UART, which is often conflated with the overall "serial" nature of the hardware._

## Getting started

Follow [these instructions](https://github.com/sbcshop/Air-Monitoring-HAT#enable-i2c-and-serial-interface) to enable serial comms. You don't need to enable I2C to use this particular sensor or serial comms in general, but you will need to restart the Pi as prompted.

```sh
# check the serial port exists
ls /dev/ttyS0

# make sure you can access it
sudo usermod -aG <user> dialout
```

Restart your shell in for the change to take effect.

## Example Sensors

### PyPMSSensor

Snsary includes an adapter for [the excellent PyPMS library](https://github.com/avaldebe/PyPMS), which knows how to configure and read from a variety of Particulate Matter Sensors (PMS). PyPMS also has its own CLI.

Example usage: [see the API docs](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/pypms/index.html)

Example device: [PMSA003 Air Monitoring HAT for Raspberry Pi](https://thepihut.com/products/air-monitoring-hat-for-raspberry-pi-pmsa003)

<details>
  <summary>Using PyPMS CLI to check a sensor works outside of Snsary</summary>

  ```bash
  pms --debug -m PMSx003 -s /dev/ttyS0 -i 5 serial
  ```

  You should eventually see a line that looks like this:

  > 2021-11-26 23:40:31: PM1 1.0, PM2.5 8.0, PM10 8.0 μg/m3

  It's worth noting the `DEBUG` output: it takes several seconds for the device to respond to the `wake` command; the device also returns a lot of garbage output initially, before valid readings come through.
</details>

_Note: Adafruit have a UART driver for PMSs, but [it doesn't seem to work for the example device](https://github.com/adafruit/Adafruit_CircuitPython_PM25/issues/9). PyPMS is more thoroughly tested and offers significant compatibility with a range of PMS devices._
