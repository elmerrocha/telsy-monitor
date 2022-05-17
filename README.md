# **Telsy Monitor**
Vital signs monitor firmware of Telsy Hogar

Copyright (C) 2022  Elmer Eduardo Rocha Jaime, Dirección de Innovación y Desarrollo Tecnológico - Fundación Cardiovascular de Colombia FCV

## **📑 Menu**
- [📋 Requirements](#-requirements)
- [💾 Raspberry Pi OS Installation](#-raspberry-pi-os-installation-on-microsd)
- [🔧 Raspberry Pi OS Setup](#-raspberry-pi-os-setup)
- [⚙️ Change boot image](#%EF%B8%8F-change-boot-image)
- [🚀 Starting](#-starting)
- [🛠️ Built with](#%EF%B8%8F-built-with)
- [✒️ Autors](#%EF%B8%8F-autors)
- [📄 License](#-license)

## **📋 Requirements**
This is what is necessary to run the project:
- [Raspberry Pi 4 Model B 4GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- [Raspberry Pi OS with desktop - Debian 10 Buster (May 7th 2021)](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/)
- [Python 3.7.3](https://www.python.org/downloads/release/python-373/)
- [Django 3.2.13](https://docs.djangoproject.com/en/4.0/releases/3.2.13/)

Python libraries needed:
- [wifi](https://pypi.org/project/wifi/)
- [pytz](https://pypi.org/project/pytz/)
- [smbus](https://pypi.org/project/smbus/)
- [pyserial](https://pypi.org/project/pyserial/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)

## **💾 Raspberry Pi OS installation on microSD**
These installation instructions are written for the Windows 10 operating system.

It's necessary a microSD with more than 8 GB and a SD Adapter or a microSD USB adapter.


### Step 1. Download the [Raspberry Pi Imager program](https://www.raspberrypi.com/software/) and install it

![Download Raspberry Pi Imager](/telsy/monitor/static/images/installation/download_raspberry_pi_imager.png)

### Step 2. Download the OS image
Scroll down in the [page](https://www.raspberrypi.com/software/) and go to [See all download options](https://www.raspberrypi.com/software/operating-systems/), in the Operating system images section go to [`Raspberry Pi OS with desktop`](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit) and click on [Archive](https://downloads.raspberrypi.org/raspios_armhf/images/).

![Archive Raspberry Pi OS with desktop](/telsy/monitor/static/images/installation/raspberry_pi_os_with_desktop.png)

In archive page select [`raspios_armhf-2021-05-28`](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/), once there download the [`2021-05-07-raspios-buster-armhf.zip`](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip) file.

![2021-05-07-raspios-buster-armhf](/telsy/monitor/static/images/installation/2021-05-07-raspios-buster-armhf.png)

### Step 3. Setup Raspberry Pi Imager
At the Raspberry Pi Imager program click on `CHOOSE OS` button, now go to `Use custom`, there select the OS image file downloaded (2021-05-07-raspios-buster-armhf.zip).

![Use custom OS image](/telsy/monitor/static/images/installation/use_custom_image.png)

Now select the microSD clicking on `CHOOSE STORAGE`, after press the gear (⚙️) button, in the _Set hostname:_ write **monitor**, select `Enable SSH`.

![Setup Hostname](/telsy/monitor/static/images/installation/setup_hostname.png)

Now select `Set username and password`, in _Username_ write **telsy** and create a password. Configure wireless LAN or connect the Raspberry Pi 4 to Internet by Ethernet.

![Setup username](/telsy/monitor/static/images/installation/setup_username.png)

If you configured a Wireless LAN network select **CO** in `Wireless LAN country`, press in `Set locale settings` select **America/Bogota** and **latam** in `Keyboard layout`. Then press `SAVE` button.

![Setup locale and time zone](/telsy/monitor/static/images/installation/setup_locale.png)

After all press `WRITE` button to start the microSD writing.

### Step 4. Start Raspberry Pi OS

First put the microSD in the Raspberry Pi 4, connect the touchscreen or screen and  power the board. If you configured wireless LAN connection you have to look for the Raspberry Pi IP by the name `monitor`.

## **🔧 Raspberry Pi OS Setup**

### Step 1. Welcome to Raspberry Pi
When you power the Raspberry Pi board for the first time you see the window called _Welcome to Raspberry Pi_ press Next to start the setup.

![Welcome to Raspberry Pi 1](/telsy/monitor/static/images/installation/welcome_to_raspberry_1.png)

At the `Set Country` part in _Country_ select **Colombia** and press _Next_. After that it will ask to change password press _Next_ to skip this step. Then if you have a trouble with black border in the screen select _This screen shows a black border around the desktop_ and press _Next_, skip the WiFi network configuration if the Raspberry Pi board is connected to internet already.

After all you will see the _Update Software_ it's recommended update it and reboot after it has finished.

### Step 2. Login to the Raspberry over SSH
The pi user is called `telsy`, so the way to login over ssh is:
```
ssh telsy@raspberry.ip
```
The program will ask you for a ED25 key fingerprint, so you have to write *yes* and continue writing the user password.

![SSH Fingerprint](/telsy/monitor/static/images/installation/fingerprint.png)

### Step 3. Configure interfaces settings
Once you remotely connect to the pi over ssh, run the following command:
```
sudo raspi-config
```

![Raspi Config](/telsy/monitor/static/images/installation/raspi_config.png)

From the menu select:
- 3 Interface Options
    - P5 I2C
        - Yes
    - P6 Serial Port
        - Shell
            - No
        - Hardware
            - Yes

![Serial interface](/telsy/monitor/static/images/installation/serial_interface.png)

Press the `tab` key twice to get to the `Finish` option, then press the enter key.

When asked to reboot, select `Yes`.

Reconnect after reboot via ssh.

### Step 4. Install some components and Python libraries
While remotely logged in to the pi, run the following at the command line:
```
sudo apt-get update
```
```
sudo apt-get install -y xscreensaver plymouth plymouth-themes pix-plym-splash
```
```
sudo apt-get remove -y lxplug-ptbatt
```
```
sudo pip3 install Django==3.2.13 wifi smbus pyserial RPi.GPIO pytz
```

### Step 5. Edit the boot config.txt file
```
sudo nano /boot/config.txt
```
Check that `enable_uart=1` is on the last line, otherwise add it.

And add the following at the last line (the shortcut to paste is `Shift + Insert`):
```
disable_splash=1
dtoverlay=uart2
avoid_warnings=1
```
The last lines should look like this:

![Config.txt](/telsy/monitor/static/images/installation/config_txt.png)

Press <kbd>Ctrl+O</kbd>, then press <kbd>Enter</kbd> and press <kbd>Ctrl+X</kbd>.

### Step 6. Edit the cmdline.txt file
```
sudo nano /boot/cmdline.txt
```
Remove this (if exists):
```
console=serial0,115200
```
Add this to the end:
```
logo.nologo vt.global_cursor_default=0
```

## **⚙️ Change boot image**

### Step 1. Edit the Plymouth pix.script file
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
Press <kbd>Ctrl+O</kbd>, then press <kbd>Enter</kbd> and press <kbd>Ctrl+X</kbd>.

The last lines should look like this:

![Plymouth pix script](/telsy/monitor/static/images/installation/plymouth.png)

### Step 2. Restart
Put the command line:
```
sudo reboot
```

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
```python
def get_key():
    ''' Django key '''
    return 'django-insecure-#&g7+gw14^ux1yvk(wxftntu$ui_n&0(f#v_f+@c8l02#^d!5^'

```
Save the file pressing <kbd>Ctrl+O</kbd>, then press <kbd>Enter</kbd> and press <kbd>Ctrl+X</kbd>.


### Step 4. Change wallpaper and desktop size
Right click on the desktop go to `Desktop preferences`, then go to _Defaults_ tab and press **Set Defaults** button in front of _For small screens_.

![Set defaults for small screens](/telsy/monitor/static/images/installation/set_defaults_small_screens.png)

Then go back to _Desktop_ tab, deselect _Wastbasket_, and now press `temple.jpg` in front of _Picture_ and select **splash.jpg** in the path _/home/telsy/telsy-monitor/telsy/monitor/static/images_.

![Splash wallpaper](/telsy/monitor/static/images/installation/splash_wallpaper.png)

Now go to _Menu Bar_ tab and press the box in front of _Colour_, then in _Pick a Color_ window press the dropper button, and select whe color of the wallpaper, you will se the color code `#E8E9EE`, then press OK.

![Pick a color](/telsy/monitor/static/images/installation/pick_a_color.png)

### Step 5. Hide pointer
Put the command line:
```
sudo nano /etc/lightdm/lightdm.conf
```
Go to the 95 line, uncomment it and add -nocursor:
```
xserver-command=X -nocursor
```
It should look like this:

![Lightdm.conf](/telsy/monitor/static/images/installation/lightdm_conf.png)

### Step 6. Configure kiosk startup
Put the command line:
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Comment (add #) to _@lxpanel --profile LXDE-pi_ and add this to the last lines:
```
@sh /home/telsy/telsy-monitor/startserver.sh
@sh /home/telsy/telsy-monitor/startweb.sh
```
It should look like this:

![Autostart settings](/telsy/monitor/static/images/installation/autostart.png)


### Step 7. Disable sleep mode
Go to main menu (Raspberry Pi icon), then Preferences, then **Screensaver**, now change _Mode_ to **Disable Screen Saver** and close the window:

![Screensaver](/telsy/monitor/static/images/installation/screensaver.png)


### Step 8. Restart
Put the command line:
```
sudo reboot
```
If you followed the steps correctly you should see the Telsy Home interface.

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
This project is under the GNU AGPLv3 License - look at the file [LICENSE.md](LICENSE.md) for more details
