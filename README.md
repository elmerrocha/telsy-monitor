# Telsy Monitor

_Telsy Monitor: vital signs monitor firmware_

## Starting 🚀

_Download/clone this repository, place it in the path /home/pi/_

## Requirements 📋

### _This is what is necessary to run the project:_

```
- Raspberry Pi 4 Model B 4GB
- Raspberry Pi OS with desktop (Kernel v5.10)
- Python 3.7.3
- Django 3.2.8
- Gedit
- Unclutter
- Xscreensaver
```
### _Python libraries needed:_

```
- wifi
- pytz
```

## Installation 🔧

### _Raspbian OS:_

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install gedit
sudo apt-get install unclutter
sudo apt-get install xscreensaver
```

### _Python libraries:_

```
sudo pip3 install Django==3.2.8
sudo pip3 install wifi
sudo pip3 install pytz
sudo pip install pytz
```


## Setting ⚙️

### _Enable Serial Port, enable I2C , disable Serial Console and enable Remote GPIO:_

```
Clic on applications menu button, go to Preferences/Raspberry pi configurations/Interfaces,
then enable Serial Port, I2C , Remote GPIO, disable Serial Console and restart the system.
```

### _Enable UART on Raspbian OS: edit config.txt and add 2 lines_

```
sudo gedit /boot/config.txt
```
```
[all]
enable_uart=1
dtoverlay=uart2
```
```
sudo gedit /boot/cmdline.txt
```
```
Delete console=tty1
```

### _Hide pointer: edit lightdm.conf, uncomment xserver-command=X and add -nocursor (line 95)_

```
sudo gedit /etc/lightdm/lightdm.conf
```
```
[Seat:*]
#type=local
#pam-service=lightdm
#pam-autologin-service=lightdm-autologin
#pam-greeter-service=lightdm-greeter
#xserver-backend=
xserver-command=X -nocursor
```

### _Disable auto-shutdown and kiosk startup: edit autostart_

```
sudo gedit /etc/xdg/lxsession/LXDE-pi/autostart
```
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@sh /home/pi/telsy-monitor/startserver.sh
@sh /home/pi/telsy-monitor/startweb.sh
```

### _Disable sleep mode:_

```
Clic on applications menu button, go to Preferences/Screensaver and change mode to "Disable Screen Saver"
```

## Built with  🛠️

* [Django](https://docs.djangoproject.com/en/3.2/) - Web Framework
* [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) - CSS Framework
* [Fontawesome](https://fontawesome.com/v6.0/icons) - Icons
* [jQuery](https://api.jquery.com/) - JavaScript API
* [Splide](https://splidejs.com/category/users-guide/) - JavaScript Slider
* [WiFi](https://pypi.org/project/python-wifi/) - Wifi python library
* [pytz](https://pypi.org/project/pytz/) - Date/Timezone library


## Autors ✒️

* **Juan Sebastián Barrios** - *Graphic interface* - [s3ba5t1an](https://github.com/s3ba5t1an)
* **David Vásquez** - *API / Telecentre platform* - [davidvasquezr](https://github.com/davidvasquezr)
* **Elmer Rocha** - *Monitor firmware* - [elmerrocha](https://github.com/elmerrocha)


## License 📄

This project is under the MIT License - look aht the file [LICENSE.md](LICENSE.md) for more details