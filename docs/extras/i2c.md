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

### Adafruit

Example usage: [see the API docs](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/adafruit/index.html)

#### BH1750 Light Sensor

- [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-bh1750-ambient-light-sensor.pdf)
- [Shop link](https://thepihut.com/products/adafruit-bh1750-light-sensor-stemma-qt-qwiic)

This works out the box - the Adafruit library sets it up for [continuous reading at high resolution](https://github.com/adafruit/Adafruit_CircuitPython_BH1750/blob/9d5fabd77185a81cf06451b3fbdbaf518a1f4727/adafruit_bh1750.py#L195-L196). I don't have any other sensors to compare with, but the readings are consistent with the time of day and amount of sunlight.

#### Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor

- [Datasheet](https://cdn-learn.adafruit.com/assets/assets/000/098/461/original/Sensirion_CO2_Sensors_SCD30_Datasheet.pdf?1609871944)
- [Shop link](https://thepihut.com/products/adafruit-scd-30-ndir-co2-temperature-and-humidity-sensor)

<details>
<summary>Calibration example program for the SCD30</summary>

```python
import board
import adafruit_scd30

i2c = board.I2C()
device = adafruit_scd30.SCD30(i2c, address=0x61)

# Leave as-is (0). Changing the pressure had no
# noticeable effect on the reported CO2 readings.
# device.ambient_pressure = 0  # original was "0"

# Disable auto calibration of CO2. This relies on
# daily, prolongued exposure to fresh air, which
# isn't a reliable assumption for a typical home.
device.self_calibration_enabled = False

# Run this after exposing the device to fresh air
# for 30 minutes i.e. next to an open window. May
# need to repeat to get "400" as the average.
device.forced_recalibration_reference = 400

# This is a negative offset to compensate for the
# local heating of the circuit board. I use an
# analogue, indoor thermometer for comparison.
device.temperature_offset = 5  # original was "0"
```
</details>

The temperature readings are highly sensitive to the position of the SCD30. Even with plenty of ventilation, changing where the sensor is mounted would affect the reported temperature by up to 1°C.

Note: [the driver example makes use of a `data_available` property](https://github.com/adafruit/Adafruit_CircuitPython_SCD30/blob/b3d9bd141ae86ec4f871ae42a35d208003672c02/examples/scd30_simpletest.py#L17), but I've not found this necessary - probably because the poll interval (10 seconds) is greater than the measurement interval ([2 seconds](https://github.com/adafruit/Adafruit_CircuitPython_SCD30/blob/b3d9bd141ae86ec4f871ae42a35d208003672c02/adafruit_scd30.py#L98)).

#### Adafruit MS8607 Pressure Humidity Temperature PHT Sensor

- [Datasheet](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Data+Sheet%7FMS8607-02BA01%7FB3%7Fpdf%7FEnglish%7FENG_DS_MS8607-02BA01_B3.pdf%7FCAT-BLPS0018)
- [Shop link](https://thepihut.com/products/adafruit-ms8607-pressure-humidity-temperature-pht-sensor)

This works for **pressure** out the box - the Adafruit library sets it up to [read at the highest resolution](https://github.com/adafruit/Adafruit_CircuitPython_MS8607/blob/1d08d0d09f0c556c71bb19c9816e6efb59aead65/adafruit_ms8607.py#L180-L185). I don't have any other sensors to compare with, but the readings are consistent with changes in weather (stormy vs. sunny).

Temperature / humidity can't be adjusted easily: the calibration values are documented in the datasheet but not in detail, and [aren't intended to be changed](https://github.com/adafruit/Adafruit_CircuitPython_MS8607/blob/1d08d0d09f0c556c71bb19c9816e6efb59aead65/adafruit_ms8607.py#L210). Not useful if the sensor is positioned near other heat sources.

#### Adafruit SGP30 Air Quality Sensor

- [Datasheet](https://cdn-learn.adafruit.com/assets/assets/000/050/058/original/Sensirion_Gas_Sensors_SGP30_Datasheet_EN.pdf)
- [Shop link](https://thepihut.com/products/adafruit-sgp30-air-quality-sensor-breakout-voc-and-eco2-ada3709)

This needs some calibration ([see API docs](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/adafruit/index.html)) but ultimately produces comparable TVOC trends and even values compared to another, benchmark VOC sensor. As with the benchmark sensor, most of the trends can be attributed to household activities. There's a fairly constant or "background" TVOC level of 100-200 unless a window is open; this makes it hard to use the sensor as a meaningful indicator of pollution in an indoor environment.

### Pimoroni

Example usage: [see the API docs](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/pimoroni/index.html)

#### MICS6814 3-in-1 Gas Sensor Breakout

- [Datasheet](https://www.sgxsensortech.com/content/uploads/2015/02/1143_Datasheet-MiCS-6814-rev-8.pdf)
- [Shop link](https://thepihut.com/products/mics6814-3-in-1-gas-sensor-breakout-co-no2-nh3)

The resistance readings from this sensor [weren't useful in practice and it's unclear if they are correct](https://github.com/pimoroni/mics6814-python/issues/4), even as relative measurements. They all change together. It's unlcear if the sensor is faulty as there are no baselines for comparison. Trying [the "Sharpie suggestion"](https://learn.pimoroni.com/article/getting-started-with-enviro-plus) only led to a negligible change in all three measurements.

## Example Outputs

### OLED display

Adafruit have provided some great APIs for OLED displays and there are many possible visualisations. Snsary doesn't provide any special code for working with OLED displays as outputs.

Example usage: [see examples/ssd1306.py](../examples/ssd1306.py), which works with the [PMSA003 Air Monitoring HAT for Raspberry Pi](https://thepihut.com/products/air-monitoring-hat-for-raspberry-pi-pmsa003). Note that the rendering library [needs a specific font](https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/043d8a75004d81e0326a6ac42ca4f71d1de94ac4/adafruit_framebuf.py#L383); see the example for instructions.
