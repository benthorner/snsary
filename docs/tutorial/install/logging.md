# Logging

_This guide is written for Grafana Cloud Loki._

## Install the log forwarder

Grafana provide a log forwarder called [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/installation/), which can be run as a binary. Download the latest binary release for `-linux-arm` and install it and the conventional directory for privileged binaries.

```bash
unzip promtail-linux-arm.zip

sudo mv promtail-linux-arm /usr/local/sbin/promtail
sudo chown root:root /usr/local/sbin/promtail
```

## Forward `/var/log/syslog`

Currently Raspian OS ships with Rsyslog pre-installed and enabled as a service, which means logs are streamed into `/var/log/syslog`. It's easy to configure Promtail to watch this file and forward the logs.

```
# /etc/promtail.yaml

server:
  disable: true

positions:
  filename: /tmp/positions.yaml

client:
  url: <loki URI with basic auth>

scrape_configs:
  - job_name: system
    static_configs:
    - targets:
        - localhost
      labels:
        job: varlogs
        __path__: /var/log/syslog
```

## Start Promtail as a service

Create a service definition for Promtail.

```
# /etc/systemd/system/promtail.service

[Unit]
Description=Promtail
Requires=time-sync.target
After=time-sync.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/local/sbin/promtail -config.file=/etc/promtail.yaml

[Install]
WantedBy=multi-user.target
```

Now enable and start the Promtail service.

```bash
sudo systemctl daemon-reload
sudo systemctl enable promtail
sudo service promtail start
```

Check to see if if starts and tail its logs:

```bash
sudo service promtail status

sudo journalctl -f -u promtail
```
