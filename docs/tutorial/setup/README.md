# Install

_Tip: before starting it's worth following some of [this article](https://raspberrytips.com/security-tips-raspberry-pi/) to secure the system. I needed to make [this adjustment](https://raspberrypi.stackexchange.com/questions/38931/how-do-i-set-my-raspberry-pi-to-automatically-update-upgrade#comment130516_38990) for the part about unattended-upgrades._

## Install system packages

```bash
sudo apt install python3-pip

# plain 'vi' has cursor issues
sudo apt install vim
```

## Setup basic snsary app

Copy [examples/basic.py](../../examples/basic.py) to `~/snsary`.

Now install the snsary package and run the app.

```bash
sudo apt install git

pip3 install git+https://github.com/benthorner/snsary#egg=snsary

./snsary
# or "python3 snsary"
```

At this point you should see some INFO logs e.g.

```bash
2021-11-13 19:07:17,144 - INFO - [mocksensor-4382645216] Collected 1 readings.
2021-11-13 19:07:17,144 - INFO - [mockoutput-4383959840] Reading: <zero 1636830437 0>
```

## Make the app a service

Run [examples/install/service.sh](../../examples/install/service.sh) (replace `<YOUR_USERNAME>`).

Check to see if the service starts and tail its logs:

```bash
sudo service snsary status

sudo journalctl -f -u snsary
```

_For long term and more convenient analysis, it's worth exporting the logs to an external service, such as [GrafanaCloud Loki](logging.md), which is free at the time of writing._

## Customising your app

Snsary makes it easy to build large sensing apps:

- [In-built processing tools e.g. filters](tools.md).
- [Extra pre-built sensors and outputs](extras.md).

[examples/contrib.py](../../examples/contrib.py) shows many of them working together. See [the rest of the tutorial](../README.md) for more details on types of Sensors and Outputs featured in this example file.
