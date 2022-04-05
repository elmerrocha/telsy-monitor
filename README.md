# **Telsy Monitor**
Telsy Monitor: vital signs monitor firmware of Telsy Hogar

Copyright (C) 2022  Elmer Eduardo Rocha Jaime, Dirección de Innovación y Desarrollo Tecnológico - Fundación Cardiovascular de Colombia FCV

## **📋 Requirements**
This is what is necessary to run the project:
- [Raspberry Pi 4 Model B 4GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- [Raspberry Pi OS Lite 32-bit - Debian 11 Bullseye (January 28th 2022)](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-01-28/)
- [Python 3.9.2](https://www.python.org/downloads/release/python-392/)
- [Django 4.0.3](https://docs.djangoproject.com/en/4.0/releases/4.0.3/)

Python libraries needed:
- [wifi](https://pypi.org/project/wifi/)
- [pytz](https://pypi.org/project/pytz/)
- [smbus](https://pypi.org/project/smbus/)

## **🔧 Raspberry Pi OS Lite Setup**
### Step 1. Login to the pi over ssh
The pi is called `telsy` the way to login over ssh is:
```
ssh telsy@raspberry.ip
```
Be sure to adjust the instructions above for the host name that you are using.

### Step 2. Configure startup settings
Once you remotely connect to the pi over ssh, run the following command:
```
sudo raspi-config
```
From the menu select:
- 1 System Options
    - S5 Boot / Auto Login
        - B2 Console Autologin
- 2 Display Options
    - D2 Underscan
        - No
- 3 Interface Options
    - I5 I2C
        - Yes
    - I6 Serial Port
        - Shell
            - Yes
        - Hardware
            - Yes

Press the `tab` key twice to get to the `Finish` option, then press the enter key.

When asked to reboot, select `Yes`.

Reconnect after reboot via ssh.

### Step 3. Install minimum GUI components
Before you can run the Chromium browser on a lite version of Raspberry Pi OS, you will need a minimum set of GUI components to support it.

While remotely logged in to the pi, run the following at the command line:
```
sudo apt-get update
```
```
sudo apt-get install -y --no-install-recommends xserver-xorg xinit x11-xserver-utils
```

### Step 4. Install Chromium Web browser
Once the minimum GUI components are in place, you can install the Chromium browser to display a Web site.
```
sudo apt-get install -y --no-install-recommends chromium-browser
```

### Step 5. Install Python pip and git
Pip is the package installer for Python. You need to use pip to install packages from the Python Package Index.

Git is needed too to clone the project and i2c to read the batteries.
```
sudo apt-get install -y python3-pip git i2c-tools
```

### Step 6. Install Python libraries
After install Chromium install all python libraries needed to run the project.
```
sudo pip install Django==4.0.3 wifi smbus pyserial serial
```

## **🖥️ Kiosk mode setup**
### Step 1. Create autostart file
Edit `/home/telsy/.bash_profile` to automatically start the GUI. There's a check for the bash context first, so you don't accidentally start chromium whenever you ssh in.
```
nano .bash_profile
```
Write the next and save the file.
```
if [ -z $DISPLAY ] && [ $(tty) == /dev/tty1 ]
then
  startx -- -nocursor >/dev/null 2>&1
fi
```
Press `Ctrl+O`, then press `Enter` and press `Ctrl+X`.

### Step 2. Configure chromium browser
Create `xinitrc` file in `/home/telsy/.xinitrc` to run chromium whenever you run startx.
```
nano .xinitrc
```
Write the next lines and save the file.
```
#!/usr/bin/env sh
xset -dpms
xset s off
xset s noblank

sh /home/telsy/telsy-monitor/startserver.sh &
sleep 5
chromium-browser http://localhost:8000 \
  --window-size=801,481 \
  --window-position=0,0 \
  --check-for-update-interval=31536000 \
  --start-fullscreen \
  --kiosk \
  --noerrdialogs \
  --disable-translate \
  --no-first-run \
  --no-context-menu \
  --disable-context-menu \
  --fast \
  --fast-start \
  --disable-infobars \
  --overscroll-history-navigation=0 \
  --disable-pinch \
  --disable-session-crashed-bubble \
  --disable-sync \
  --disable-features=TouchpadOverscrollHistoryNavigation

```
Press `Ctrl+O`, then press `Enter` and press `Ctrl+X`.

## **⚙️ Change boot image**
### Step 1. Install Plymouth for changing boot image
Once you remotely connect to the pi over ssh, run the following command to install `Plymouth` to present a graphic (bootsplash) while the system boot:
```
sudo apt-get install -y plymouth plymouth-themes pix-plym-splash
```

### Step 2. Edit the boot config.txt file
```
sudo nano /boot/config.txt
```
Check that `enable_uart=1` is on the last line, otherwise add it.

And add the following at the last line:
```
disable_splash=1
dtoverlay=uart2
```
Press `Ctrl+O`, then press `Enter` and press `Ctrl+X`.

### Step 3. Edit the Plymouth pix.script file
```
sudo nano /usr/share/plymouth/themes/pix/pix.script
```
Remove the following (stay at the line to remove and press `Ctrl+K`):
```
message_sprite = Sprite();
message_sprite.SetPosition(screen_width * 0.1, screen_height * 0.9, 10000);

my_image = Image.Text(text, 1, 1, 1);
message_sprite.SetImage(my_image);
```
Press `Ctrl+O`, then press `Enter` and press `Ctrl+X`.

### Step 4. Edit the cmdline.txt file
```
sudo nano /boot/cmdline.txt
```
Remove this:
```
console=serial0,115200
```
Add this to the end:
```
splash quiet plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0
```
Press `Ctrl+O`, then press `Enter` and press `Ctrl+X`.

## **🚀 Starting**
### Step 1. Clone the repository
Check that the current path is `/home/telsy/` (with `pwd` command), then run the next command line:
```
git clone https://github.com/elmerrocha/telsy-monitor.git
```

### Step 2. Put boot image to specific path
Run the command:
```
sudo cp /home/telsy/telsy-monitor/telsy/monitor/static/images/splash.png /usr/share/plymouth/themes/pix
```

### Step 3. Create Django key
You need to create `key.py` file in `/home/telsy/telsy-monitor/telsy/telsy/`:
```
nano /home/telsy/telsy-monitor/telsy/telsy/key.py
```
Add the next to the file:
```
def get_key():
    ''' Django key '''
    return 'django-insecure-#&g7+gw14^ux1yvk(wxftntu$ui_n&0(f#v_f+@c8l02#^d!5^'

```
Save the file pressing `Ctrl+O`, then press `Enter` and press `Ctrl+X`.
### Step 4. Restart
Put the command line:
```
sudo reboot now
```
If you followed the steps correctly you should start the Telsy Home interface.

## **🛠️ Built with**
* [Django](https://docs.djangoproject.com/en/4.0/) - Web Framework
* [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) - CSS Framework
* [Fontawesome](https://fontawesome.com/v6.0/icons) - Icons
* [jQuery](https://api.jquery.com/) - JavaScript AJAX Library
* [Splide](https://splidejs.com/category/users-guide/) - JavaScript Slider
* [Roboto](https://fonts.google.com/specimen/Roboto) - Google Typographic Fonts
* [Sweetalert](https://sweetalert.js.org/guides/) - JavaScript popup messages

## **✒️ Autors**
* **Juan Sebastián Barrios** - *Graphic interface* - [s3ba5t1an](https://github.com/s3ba5t1an)
* **David Vásquez** - *Telecentre platform* - [davidvasquezr](https://github.com/davidvasquezr)
* **Elmer Rocha** - *Monitor firmware* - [elmerrocha](https://github.com/elmerrocha)

## **📄 License**
This project is under the MIT License - look aht the file [LICENSE.md](LICENSE.md) for more details
