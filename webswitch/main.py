import time
import network
import gc
import machine
from simplewebserver import SimpleWebSwitch

def do_connect(ssid, pwd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            time.sleep_ms(200)
        print('STA config: ', sta_if.ifconfig())
    return sta_if

def do_accesspoint(ssid, pwd):
    ap_if = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=pwd)
    ap_if.active(True)
    time.sleep_ms(200)
    #print('AP config: ', ap_if.ifconfig())
    return ap_if

#----------------------------------------------------------------
# MAIN PROGRAM STARTS HERE

if __name__ == '__main__':
    sws = SimpleWebSwitch()
    sws.server()