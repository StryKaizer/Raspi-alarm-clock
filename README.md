# Raspi Alarm Clock

This project extends the Volumio project (see https://volumio.org) , triggering a specific Spotify playlist to play when a Google calendar event occurs.

This code was tested on a Raspi2 model, running Volumio 1.55

## Requirements

* Google calendar API oAuth 2 client id (Type: Other) registered at console.developers.google.com, which has google calendar API enabled.
* A machine running Volumio

## Installation

    $ wget https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py
    $ git clone https://github.com/StryKaizer/Raspi-alarm-clock.git
    $ cd Raspi-alarm-clock
    $ sudo pip install -r requirements.txt
    $ wget http://sourceforge.net/projects/salix-sbo/files/13.37/pyfeed/pyfeed-0.7.4.tar.gz
    $ tar -zxvf pyfeed-0.7.4.tar.gz
    $ cd pyfeed-0.7.4
    $ sudo python setup.py install
    
Add your Google oAuth JSON file to the project root folder using as name client_secret.json

Configure settings by editting the config.cfg file

Authenticate with your google calendar by running following command, then copy/paste the url in a browser

    $ python raspi_alarm_clock.py --noauth_local_webserver

After that, past the verification code back into the commandline

You can now test if the script works by running

    $ python raspi_alarm_clock.py

Now open cronjob configuration by running

    $ crontab -e

Add this line at the end:

    */1 * * * * /usr/bin/python2.7 /home/pi/Raspi-alarm-clock/raspi_alarm_clock.py

Volumio kills the cron daemon by default, so lets comment out that line of code by running

    $ sudo nano /var/www/command/orion_optimize.sh
    
Then find following line and add a # in front of it.

    killall -9 ntpd


Your playlist will now fire every time a Google calendar event occurs.  Goodnight!

## Credits

Created by StryKaizer
