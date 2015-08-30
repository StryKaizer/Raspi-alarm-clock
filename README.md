# Raspi-alarm-clock


This project extends the Volumio project, triggering a specific spotify playlist to play when a google calendar event occurs.


# Setup

    $ sudo pip install -r requirements.txt
    $ wget http://sourceforge.net/projects/salix-sbo/files/13.37/pyfeed/pyfeed-0.7.4.tar.gz
    $ tar -zxvf pyfeed-0.7.4.tar.gz
    $ cd pyfeed-0.7.4
    $ sudo python setup.py install

Authenticate with your google calendar by running following command, then copy/paste the url in a browser

    $ python raspi_alarm_clock.py --noauth_local_webserver

After that, past the verification code back into the commandline

You can now test if the script works by running

    $ python raspi_alarm_clock.py

Now just add the following line as a cronjob to trigger the script each minute

    $ crontab -e

Add this line at the end:

    */1 * * * * /usr/bin/python2.7 /home/pi/raspi-alarm/raspi_alarm_clock.py

