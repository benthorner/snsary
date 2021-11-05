# Serial

Raspberry Pi exposes GPIO 14+15 as a serial device.

_Note: "serial" is ambiguous. It can refer to e.g. UART, I2C, SPI, USB, etc. Here it refers to UART, which is often conflated with the overall "serial" nature of the hardware._

## First enable serial comms

Follow [these instructions](https://github.com/sbcshop/Air-Monitoring-HAT#enable-i2c-and-serial-interface) to enable serial comms. You don't need to enable I2C to use the PMS, but you will need to restart the Pi as prompted.

```sh
# check the serial port exists
ls /dev/ttyS0

# make sure you can access it
sudo usermod -aG <user> dialout
```

Restart your shell in for the change to take effect.

## Now use it for something

- [PyPMS](pypms.md): add a partice sensor (PMS).
