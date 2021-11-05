# I2C

Raspberry Pi exposes GPIO 2+3 as an I2C bus (#1).

_Note: there is another I2C bus at GPIO 0+1, which seems to be exposed as `/dev/i2c-2` but apparently shouldn't be used because it's [reserved for communication with HATs and possibly internal uses](https://raspberrypi.stackexchange.com/questions/50348/what-are-the-id-eeprom-pins-and-what-can-they-be-used-for)._

## First enable I2C comms

Follow [these instructions](https://github.com/sbcshop/Air-Monitoring-HAT#enable-i2c-and-serial-interface) to enable I2C comms. Unlike serial comms, you don't need to restart the Pi to complete the change.

```
# check the I2C port exists
ls /dev/i2c

# make sure you can access it
sudo usermod -aG i2c <user>

# optional utility to check
sudo apt install i2c-tools

# check for devices on the bus
i2cdetect -y 1
```

## Now use it for something

- [SSD13606](ssd1306.md): output to an OLED display.
- [BH1750](bh1750.md): add a light sensor.

_Warning: the Adafruit I2C library does have [a locking feature](https://github.com/adafruit/Adafruit_Blinka/blob/fa80f7d2ef51b0aea92196e96c3584512d30e64d/src/adafruit_blinka/__init__.py#L61-L66), but it's not thread-safe. This means it's possible for multiple sensors to conflict if they poll for data around the exact same time._
