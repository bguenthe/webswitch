import socket
import network
import time
import gc
import machine

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

class SimpleWebSwitch:
    PIN_LED = 2
    # Parses the client's request.
    # Returns a dictionary containing pretty much everything
    # the server needs to know about the uri.

    def __init__(self):
        self.pinLED = machine.Pin(self.PIN_LED, machine.Pin.OUT)  # an
        self.pinLED.value(1)  # aus

    def parse_request(self, req):
        if b'\r\n' not in req :
            return None

        r = {}
        line, rest = req.split(b'\n', 1)
        method, uri, http = line.split(b' ')

        Methods = b'GET HEAD POST PUT'
        if method in Methods:
            r['uri'] = uri
            r['method'] = method
            r['http'] = http
            uri = uri.replace(b'/', b'')
            r['args'] = self.get_args(uri)
            if b'?' in uri: endpos = uri.find(b'?')
            else: endpos = len(uri)
            r['file'] = uri[:endpos]

        return r

    def get_args(self, uri):
        answer = {}
        if uri == None or uri == b'' :
            return answer
        uri = bytes.decode(uri)
        if '?' in uri:
            params = uri.split('?')[1]
            if '=' in uri:
                answer = dict(item.split('=') for item in params.split('&'))
        return answer

    def do_connect(self, ssid, pwd):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.connect(ssid, pwd)
            while not sta_if.isconnected():
                time.sleep_ms(200)
            print('STA config: ', sta_if.ifconfig())
        return sta_if

    def do_accesspoint(self, ssid, pwd):
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid="wemos", authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
        time.sleep_ms(200)
        return ap

    def server(self):
        self.do_accesspoint("test", "test")

        #self.do_connect("claube", "Nismipf01!")

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print('listening on', addr)

        while True:
            cl, addr = s.accept()
            print('client connected from', addr)
            req = cl.readline()
            while True:
                line = cl.readline()
                if not line or line == b'\r\n':
                    break
            r = self.parse_request(req)
            if r == None:
                cl.sendall("Nix")
            elif r['uri'] == b'/' or r['uri'] == b'/index':
                cl.sendall("use an or aus")
            elif r['uri'] == b'/an':
                self.pinLED.value(0)  # an
                cl.sendall("an")
            elif r['uri'] == b'/aus':
                self.pinLED.value(1)  # aus
                cl.sendall("aus")

            cl.close()