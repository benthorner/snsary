# Button

_This guide is written for the [SparkFun Qwiic pHAT v2.0](https://thepihut.com/products/sparkfun-qwiic-phat-v2-0-for-raspberry-pi), which has a button that's exposed at GPIO 17._

## First install dependencies

```
# general APIs for GPIO, I2C, etc.
pip3 install Adafruit-Blinka
```

## Read the value of the button

Follow this tutorial: [learn.adafruit.com/circuitpython-on-raspberrypi-linux](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux).

_Note: if you see a "no access to /dev/mem" error, this is misleading. The device that's actually in use is `/dev/gpio*`. It looks like the error is [historical](https://sourceforge.net/p/raspberry-gpio-python/tickets/115/), from when `/dev/mem` was actually used._
