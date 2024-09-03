# Docs
___

## How to set up the datasender with systemd

-The systemd files can be found in : `/lib/systemd/system`
-`sudo vim name.service`
-There you will need **sudo** privlages to edit the file you made mine looks like this:

```
[Unit]
Description=This Service Runs to broadcast the cpu and gpu usage of machine
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/home/kuba/DataSender/InfoDisplay
ExecStart=/usr/bin/python3 /home/kuba/DataSender/InfoDisplay/broadcaster_nvidia.py 10.35.242.247 12347 12345
Restart=on-failure
User=kuba

[Install]
WantedBy=multi-user.target
```

-then you start the service `sudo systemctl status data_sender.service`
-the you reload **daemon** `systemctl daemon-reload`

-if you ever need to check the the status it can be doe this way `sudo systemctl status data_sender.service`
-if you ever need to restart the service it can be done by `sudo systemctl restart data_sender.service`
