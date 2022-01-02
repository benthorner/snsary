# Tutorial

Written for a Raspbery Pi 3B+.

_Tip: before starting it's worth following some of [this article](https://raspberrytips.com/security-tips-raspberry-pi/) to secure the system. I needed to make [this adjustment](https://raspberrypi.stackexchange.com/questions/38931/how-do-i-set-my-raspberry-pi-to-automatically-update-upgrade#comment130516_38990) for the part about unattended-upgrades._

## Install system packages

```bash
sudo apt install python3-pip

# plain 'vi' has cursor issues
sudo apt install vim
```

## Setup basic snsary app

See [the README](../../README.md) for an example.

## Make the app a service

Run the following (replace `<YOUR_USERNAME>`):

```bash
echo "
[Unit]
Description=Snsary
Requires=time-sync.target
After=time-sync.target

[Service]
User=ben
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

_For long term and more convenient analysis, it's worth exporting the logs to an external service, such as [GrafanaCloud Loki](logging.md), which is free at the time of writing._
