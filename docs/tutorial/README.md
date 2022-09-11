# Tutorial

Written for a Raspbery Pi 3B+.


## 1. Setup the Raspberry Pi

Install system packages:

```bash
sudo apt install python3-pip

# plain 'vi' has cursor issues
sudo apt install vim
```

It's also worth following some of [this article](https://raspberrytips.com/security-tips-raspberry-pi/) to help ensure the Raspbery Pi is secure. Note that I needed to make [this adjustment](https://raspberrypi.stackexchange.com/questions/38931/how-do-i-set-my-raspberry-pi-to-automatically-update-upgrade#comment130516_38990) for the part about unattended-upgrades to work properly.

## 2. Install sensor hardware

An example build using some of the sensors in [docs/extras](../extras/README.md) looks like this.

![Build (front)](./images/build_diag_front.JPG "Build (front)")

One of the design goals for this build was for all the hardware to stack together to create a single, self-contained structure. Another goal was to use pluggable components to avoid soldering.

[Learn more about the design goals and components used in this build](./build.md).

## 3. Run snsary as a service

First create a basic snsary Python app. See [the README](../../README.md) for an example.

To make the app a service, run the following (replace `<YOUR_USERNAME>`):

```bash
echo "
[Unit]
Description=Snsary
Requires=time-sync.target
After=time-sync.target

[Service]
User=<YOUR_USERNAME>
Type=simple
Restart=always
RestartSec=60
ExecStart=/home/<YOUR_USERNAME>/snsary

[Install]
WantedBy=multi-user.target
" | sudo tee -a /etc/systemd/system/snsary.service > /dev/null
```

Check to see if the service starts and tail its logs:

```bash
sudo systemctl daemon-reload
sudo systemctl enable snsary
sudo service snsary start
sudo service snsary status

sudo journalctl -f -u snsary
```

It's worth exporting logs to an external service, such as [GrafanaCloud Loki](logging.md).
