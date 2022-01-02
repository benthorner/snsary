# GPIO

Raspberry Pi has lots of non-specific GPIO ports.

## Getting started

```bash
sudo usermod -aG gpio <user>
```

_Note: if you see a "no access to /dev/mem" error, this is misleading. The device that's actually in use is `/dev/gpio*`. It looks like the error is [historical](https://sourceforge.net/p/raspberry-gpio-python/tickets/115/), from when `/dev/mem` was actually used._

## Example Sensors

### Button

Example usage: [see examples/button.py](../examples/button.py), which works with the [SparkFun Qwiic pHAT v2.0](https://thepihut.com/products/sparkfun-qwiic-phat-v2-0-for-raspberry-pi), which has a button that's exposed at GPIO 17. The example is based on [this Adafruit tutorial](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/digital-i-o).
