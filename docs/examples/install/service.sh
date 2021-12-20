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

sudo systemctl daemon-reload
sudo systemctl enable snsary
sudo service snsary start
