# homeassistant_edenic
Send data from Bluelab Edenic to Home Assistant


## Install
Clone the respository: `git clone git@github.com:farm-urban/homeassistant_edenic.git`
Create the python virtual environment:
```cd homeassistant_edenic
python -m venv ./venv
source ./venv/bin/activate
pip install paho-mqtt requests pyyaml
```

Edit ```edenic.yml``` to set the variables required.

Edit ```edenic.service``` to set the correct paths and install with:

```
sudo cp edenic.service /etc/systemd/system/edenic.service
sudo systemctl daemon-reload
sudo systemctl start edenic.service
```
