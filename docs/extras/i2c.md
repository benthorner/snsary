# I2C

Raspberry Pi exposes GPIO 2+3 as an I2C bus (#1).

_Note: there is another I2C bus at GPIO 0+1, which seems to be exposed as `/dev/i2c-2` but apparently shouldn't be used because it's [reserved for communication with HATs and possibly internal uses](https://raspberrypi.stackexchange.com/questions/50348/what-are-the-id-eeprom-pins-and-what-can-they-be-used-for)._

## Getting started

Follow [these instructions](https://github.com/sbcshop/Air-Monitoring-HAT#enable-i2c-and-serial-interface) to enable I2C comms.

Unlike serial comms, you don't need to restart the Pi to complete the change.

```bash
# check the I2C port exists
ls /dev/i2c

# make sure you can access it
sudo usermod -aG i2c <user>

# optional utility to check
sudo apt install i2c-tools

# check for devices on the bus
i2cdetect -y 1
```

## Example Sensors

### AdafruitSensor

Example usage: [see the API docs](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/adafruit/index.html)

## Example Outputs

### OLED display

Adafruit have provided some great APIs for OLED displays and there are many possible visualisations. Snsary doesn't provide any special code for working with OLED displays as outputs.

Example usage: [see examples/ssd1306.py](../examples/ssd1306.py), which works with the [PMSA003 Air Monitoring HAT for Raspberry Pi](https://thepihut.com/products/air-monitoring-hat-for-raspberry-pi-pmsa003). Note that the rendering library [needs a specific font](https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/043d8a75004d81e0326a6ac42ca4f71d1de94ac4/adafruit_framebuf.py#L383); see the example for instructions.
