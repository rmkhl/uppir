import network
import ntptime
from machine import RTC, Pin
import urequests

import config

# Disable Access Point
def disable_ap():
    print('Disabling access point...')
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    print('Accespoint disabled')

# Connect to the wifi
def connect_wifi(essid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print()
    print('Config:', wlan.ifconfig())
    return wlan


# Setup the gpio pin for reading and return function
# that will return the status (if timeout since last
# change has elapsed)
_last_active = 0


def setup_pir(pin, threshold_time):
    print('Configuring PIR...')
    Pin(pin, Pin.IN)

    def activity():
        return Pin(pin).value()

    print()
    return activity


def setup_slack(webhook):
    def send(mesg):
        urequests.post(webhook, json={"text": mesg})

    return send


disable_ap()
wlan = connect_wifi(config.WIFI_SSID, config.WIFI_PSWD)
motion_detected = setup_pir(config.PIR_GPIO, 0)
slack_notification = setup_slack(config.SLACK_HOOK)
#
#slack_notification("PIR online")
