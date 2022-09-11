# Build

_This guide is about the following build._

| Front | Back |
| - | - |
| ![Build (front)](./images/build_side.JPG "Build (front)") | ![Build (back)](./images/build_diag_back.JPG "Build (back)") |

## Goal: stackable hardware

The build starts off as a tower structure above the Raspberry Pi:

- 1 x [PMSA003 Air Monitoring HAT](https://thepihut.com/products/air-monitoring-hat-for-raspberry-pi-pmsa003) (bottom)
- 1 x [SparkFun Qwiic pHAT v2.0](https://thepihut.com/products/sparkfun-qwiic-phat-v2-0-for-raspberry-pi) (top)

Qwiic-compatible sensors are mounted on top using standoffs:

- 1 x [Raspberry Pi Standoff Set - 11mm](https://thepihut.com/products/raspberry-pi-standoff-set-11mm):
  - 4 x 11mm female-male standoffs
  - 4 x 11mm female-female standoffs (2 used)
  - 4 x screws

Two female-female standoffs are screwed to the Qwiic HAT from below, forming two pillars with other sensors screwed on top using the female-male standoffs, making a tower.

Note that for this to work the holes punched in the individual sensors must be spaced the same as those in the Qwiic HAT. Adafruit sensors work well, except the [SCD-30 - NDIR CO2 sensor](https://thepihut.com/products/adafruit-scd-30-ndir-co2-temperature-and-humidity-sensor) is too long to mount horizontally - it pokes out of the frame - so brackets are used to mount it vertically:

- 2 x 11mm female-female standoffs (see above)
- 4 x screws (see below, included with standoffs)
- 1 x [ETTINGER - 05.60.125 - CUBE STANDOFF, THREADED, 2XM2.5](https://www.ebay.co.uk/itm/181883221670):
  - 4 x cube standoffs (2 used)

## Goal: self-contained structure

The build has four open sides to let light in and to let air circulate.

The build has four standoff pillars at each corner of the Raspberry Pi, which provide some protection for the hardware. The pillars also make the unit easier to hold and transport, acting as a frame around which some kind of protective material can be wound. A sheet of acrylic - part of a Raspberry Pi case kit - is screwed on top of the pillars to keep them rigid, as well as providing further protection from above.

Beneath the Raspberry Pi is another sheet of acrylic - also part of the above case kit - to protect the unit from below. The sheet is separated from the Raspberry Pi using four "short" standoffs, which the pillars screw into. The "short" standoffs screw into 16mm female-female standoffs, which act as feet.

Parts list:

- 8 x [Brass M2.5 Standoffs 16mm tall - Black Plated - Pack of 2](https://thepihut.com/products/brass-m2-5-standoffs-16mm-tall-black-plated-pack-of-2):
  - 16 x female-male standoffs
- 1 x [Raspberry Pi Standoff Set - 16mm](https://thepihut.com/products/16mm-standoff-kit-for-raspberry-pi):
  - 4 x 16mm female-female standoffs
  - 8 x screws (4 used above)
- 1 x [Universal HAT Size Case DIY Kit](https://www.amazon.co.uk/Geekworm-Raspberry-Protective-Acrylic-Expansion/dp/B074T7D1V5/ref=sr_1_29?keywords=raspberry+pi+case+3b&qid=1639783682&sr=8-29):
  - 2 x acrylic sheets
  - 4 x 16mm female-male standoffs
  - 4 x 11mm female-male standoffs
  - 4 x "short" female-male standoffs
  - 4 x hand-operated screws


Note that the thickness of the HATs contributes to the height of two of the pillars, causing the final structure to be slighly crooked at the top. However, this is barely noticeable with two HATs.

## Goal: pluggable components

The build uses Stemma QT / Qwiic cables to connect most sensors:

- 4 x [STEMMA QT / Qwiic Compatible JST-SH 4-Pin Cable (50mm)](https://thepihut.com/products/stemma-qt-qwiic-jst-sh-4-pin-cable)

Using Stemma QT / Qwiic connectors gives the greatest choice of sensor hardware for Raspberry Pi compared to Grove connectors, [where the product range is centred around Arduino](https://www.tomshardware.com/features/stemma-vs-qwiic-vs-grove-connectors).

Stemma QT / Qwiic also support daisy-chaining of connectors, with many sensors having multiple sockets to accommodate this. Although it's not used in the build, it's an advantage.

Stemma QT / Qwiic connectors are different to Grove connectors, but the pin layout is the same so it would be possible to connect sensors with Grove sockets using [an adapter cable](https://thepihut.com/products/grove-to-stemma-qt-qwiic-jst-sh-cable-100mm-long).
