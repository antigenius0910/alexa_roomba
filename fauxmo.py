#!/usr/bin/env python

"""
The MIT License (MIT)

Copyright (c) 2015 Maker Musings

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# For a complete discussion, see http://www.makermusings.com
# TODO(semartin): investigate time.sleep usage in here...

import email.utils
import requests
import select
import socket
import struct
import sys
import time
import urllib
import uuid
import logging
import serial
import time
import create

# define silence
#r = 30

# map note names in the lilypad notation to irobot commands
#c4 = 60
#cis4 = des4 = 61
#d4 = 62
#dis4 = ees4 = 63
#e4 = 64
#f4 = 65
#fis4 = ges4 = 66
#g4 = 67
#gis4 = aes4 = 68
#a4 = 69
#ais4 = bes4 = 70
#b4 = 71
#c5 = 72
#cis5 = des5 = 73
#d5 = 74
#dis5 = ees5 = 75
#e5 = 76
#f5 = 77
#fis5 = ges5 = 78
#g5 = 79
#gis5 = aes5 = 80
#a5 = 81
#ais5 = bes5 = 82
#b5 = 83
#c6 = 84
#cis6 = des6 = 85
#d6 = 86
#dis6 = ees6 = 87
#e6 = 88
#f6 = 89
#fis6 = ges6 = 90

# define some note lengths
# change the top MEASURE (4/4 time) to get faster/slower speeds
#MEASURE = 160
#HALF = MEASURE/2
#Q = MEASURE/4
#E = MEASURE/8
#Ed = MEASURE*3/16
#S = MEASURE/16

#MEASURE_TIME = MEASURE/64.


# This XML is the minimum needed to define one of our virtual switches
# to the Amazon Echo

SETUP_XML = """<?xml version="1.0"?>
<root>
  <device>
    <deviceType>urn:MakerMusings:device:controllee:1</deviceType>
    <friendlyName>%(device_name)s</friendlyName>
    <manufacturer>Belkin International Inc.</manufacturer>
    <modelName>Emulated Socket</modelName>
    <modelNumber>3.1415</modelNumber>
    <UDN>uuid:Socket-1_0-%(device_serial)s</UDN>
  </device>
</root>
"""


def dbg(msg):
    logging.debug(msg)


# A simple utility class to wait for incoming data to be
# ready on a socket.

class poller:
    def __init__(self):
        self.poller = select.poll()
        self.targets = {}

    def add(self, target, fileno = None):
        if not fileno:
            fileno = target.fileno()
        self.poller.register(fileno, select.POLLIN)
        self.targets[fileno] = target

    def remove(self, target, fileno = None):
        if not fileno:
            fileno = target.fileno()
        self.poller.unregister(fileno)
        del(self.targets[fileno])

    def poll(self, timeout = 0):
        ready = self.poller.poll(timeout)
        num = len(ready)
        for one_ready in ready:
            target = self.targets.get(one_ready[0], None)
            if target:
                target.do_read(one_ready[0])
        return num


# Base class for a generic UPnP device. This is far from complete
# but it supports either specified or automatic IP address and port
# selection.

class upnp_device(object):
    this_host_ip = None

    @staticmethod
    def local_ip_address():
        if not upnp_device.this_host_ip:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                temp_socket.connect(('8.8.8.8', 53))
                upnp_device.this_host_ip = temp_socket.getsockname()[0]
            except:
                upnp_device.this_host_ip = '127.0.0.1'
            del(temp_socket)
            dbg("got local address of %s" % upnp_device.this_host_ip)
        return upnp_device.this_host_ip


    def __init__(self, listener, poller, port, root_url, server_version, persistent_uuid, other_headers = None, ip_address = None):
        self.listener = listener
        self.poller = poller
        self.port = port
        self.root_url = root_url
        self.server_version = server_version
        self.persistent_uuid = persistent_uuid
        self.uuid = uuid.uuid4()
        self.other_headers = other_headers

        if ip_address:
            self.ip_address = ip_address
        else:
            self.ip_address = upnp_device.local_ip_address()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(5)
        if self.port == 0:
            self.port = self.socket.getsockname()[1]
        self.poller.add(self)
        self.client_sockets = {}
        self.listener.add_device(self)

    def fileno(self):
        return self.socket.fileno()

    def do_read(self, fileno):
        if fileno == self.socket.fileno():
            (client_socket, client_address) = self.socket.accept()
            self.poller.add(self, client_socket.fileno())
            self.client_sockets[client_socket.fileno()] = (client_socket, client_address)
        else:
            data, sender = self.client_sockets[fileno][0].recvfrom(4096)
            if not data:
                self.poller.remove(self, fileno)
                del(self.client_sockets[fileno])
            else:
                self.handle_request(data, sender, self.client_sockets[fileno][0], self.client_sockets[fileno][1])

    def handle_request(self, data, sender, socket, client_address):
        pass

    def get_name(self):
        return "unknown"

    def respond_to_search(self, destination, search_target):
        dbg("Responding to search for %s" % self.get_name())
        date_str = email.utils.formatdate(timeval=None, localtime=False, usegmt=True)
        location_url = self.root_url % {'ip_address' : self.ip_address, 'port' : self.port}
        message = ("HTTP/1.1 200 OK\r\n"
                  "CACHE-CONTROL: max-age=86400\r\n"
                  "DATE: %s\r\n"
                  "EXT:\r\n"
                  "LOCATION: %s\r\n"
                  "OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n"
                  "01-NLS: %s\r\n"
                  "SERVER: %s\r\n"
                  "ST: %s\r\n"
                  "USN: uuid:%s::%s\r\n" % (date_str, location_url, self.uuid, self.server_version, search_target, self.persistent_uuid, search_target))
        if self.other_headers:
            for header in self.other_headers:
                message += "%s\r\n" % header
        message += "\r\n"
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.sendto(message, destination)


# This subclass does the bulk of the work to mimic a WeMo switch on the network.

class fauxmo(upnp_device):
    @staticmethod
    def make_uuid(name):
        return ''.join(["%x" % sum([ord(c) for c in name])] + ["%x" % ord(c) for c in "%sfauxmo!" % name])[:14]

    def __init__(self, name, listener, poller, ip_address, port, action_handler = None):
        self.serial = self.make_uuid(name)
        self.name = name
        self.ip_address = ip_address
        persistent_uuid = "Socket-1_0-" + self.serial
        other_headers = ['X-User-Agent: redsonic']
        upnp_device.__init__(self, listener, poller, port, "http://%(ip_address)s:%(port)s/setup.xml", "Unspecified, UPnP/1.0, Unspecified", persistent_uuid, other_headers=other_headers, ip_address=ip_address)
        if action_handler:
            self.action_handler = action_handler
        else:
            self.action_handler = self
        dbg("FauxMo device '%s' ready on %s:%s" % (self.name, self.ip_address, self.port))

    def get_name(self):
        return self.name

#    def play_starwars(robot):
#        starwars1 = [(a4,Q), (a4,Q), (a4,Q), (f4,Ed), (c5,S), (a4,Q), (f4,Ed), (c5,S), (a4,HALF)]
#        starwars2 = [(e5,Q), (e5,Q), (e5,Q), (f5,Ed), (c5,S),(aes4,Q), (f4,Ed), (c5,S), (a4,HALF)]
#        starwars3 = [(a5,Q), (a4,Ed), (a4,S), (a5,Q), (aes5,E), (g5,E),(ges5,S), (f5,S), (ges5,S)]
#        starwars4 = [(r,E), (bes4,E), (ees5,Q), (d5,E), (des5,E),(c5,S), (b4,S), (c5,E), (c5,E)]
#        starwars5 = [(r,E), (f4,E), (aes4,Q), (f4,Ed), (aes4,S),(c5,Q), (a4,Ed), (c5,S), (e5,HALF)]
#        starwars6 = [(r,E), (f4,E), (aes4,Q), (f4,Ed), (c5,S),(a4,Q), (f4,Ed), (c5,S), (a4,HALF)]
#        print("uploading songs")
#        robot.setSong( 1, starwars1 )
#        robot.setSong( 2, starwars2 )
#        robot.setSong( 3, starwars3 )
#        time.sleep(2.0)
#        print("playing part 1")
#        robot.playSongNumber(1)
#        time.sleep(MEASURE_TIME*2.01)
#        print("playing part 2")
#        robot.playSongNumber(2)
#        time.sleep(MEASURE_TIME*2.01)
#        print("playing part 3")
#        robot.playSongNumber(3)
#        robot.setSong( 1, starwars4 )
#        time.sleep(MEASURE_TIME*1.26)
#        print("playing part 4")
#        robot.playSongNumber(1)
#        robot.setSong( 2, starwars5 )
#        time.sleep(MEASURE_TIME*1.15)
#        print("playing part 5")
#        robot.playSongNumber(2)
#        robot.setSong( 3, starwars3 )
#        time.sleep(MEASURE_TIME*1.76)
#        print("playing part 3 again")
#        robot.playSongNumber(3)
#        robot.setSong( 2, starwars6 )
#        time.sleep(MEASURE_TIME*1.26)
#        print("playing part 4 again")
#        robot.playSongNumber(1)
#        time.sleep(MEASURE_TIME*1.15)
#        print("playing part 6")
#        robot.playSongNumber(2)
#        time.sleep(MEASURE_TIME*1.76)
#        print("done")


    def handle_request(self, data, sender, socket, client_address):
        if data.find('GET /setup.xml HTTP/1.1') == 0:
            dbg("Responding to setup.xml for %s" % self.name)
            xml = SETUP_XML % {'device_name' : self.name, 'device_serial' : self.serial}
            date_str = email.utils.formatdate(timeval=None, localtime=False, usegmt=True)
            message = ("HTTP/1.1 200 OK\r\n"
                       "CONTENT-LENGTH: %d\r\n"
                       "CONTENT-TYPE: text/xml\r\n"
                       "DATE: %s\r\n"
                       "LAST-MODIFIED: Sat, 01 Jan 2000 00:01:15 GMT\r\n"
                       "SERVER: Unspecified, UPnP/1.0, Unspecified\r\n"
                       "X-User-Agent: redsonic\r\n"
                       "CONNECTION: close\r\n"
                       "\r\n"
                       "%s" % (len(xml), date_str, xml))
            socket.send(message)
        elif data.find('SOAPACTION: "urn:Belkin:service:basicevent:1#SetBinaryState"') != -1:
            success = False
            if data.find('<BinaryState>1</BinaryState>') != -1:
                # on
                dbg("Responding to ON for %s" % self.name)
                print "echo test123 on!"
                ###
                ROOMBA_PORT = "/dev/ttyUSB0"
                robot = create.Create(ROOMBA_PORT)
                robot.toSafeMode()
                robot.play_starwars()
                #fauxmo.play_starwars(robot)
                robot.close()

                ser = serial.Serial('/dev/ttyUSB0', 115200)
                ser.close()

                ser.open()
                ser.write(chr(128)) # 128: start command
                ser.write(chr(131)) # 131: safe command
                time.sleep(1)
                ser.write(chr(135)) # 135: clean command
                ser.close()
                ###

                success = self.action_handler.on(client_address[0], self.name)
            elif data.find('<BinaryState>0</BinaryState>') != -1:
                # off
                dbg("Responding to OFF for %s" % self.name)
                print "echo test123 off!"
                ###
                ser = serial.Serial('/dev/ttyUSB0', 115200)
                ser.close()

                ser.open()
                ser.write(chr(128)) # 128: start command
                ser.write(chr(131)) # 131: safe command
                ser.write(chr(133)) # 135: power off command
                ser.close()
                ###

                success = self.action_handler.off(client_address[0], self.name)
            else:
                dbg("Unknown Binary State request:")
                dbg(data)
            if success:
                # The echo is happy with the 200 status code and doesn't
                # appear to care about the SOAP response body
                soap = ""
                date_str = email.utils.formatdate(timeval=None, localtime=False, usegmt=True)
                message = ("HTTP/1.1 200 OK\r\n"
                           "CONTENT-LENGTH: %d\r\n"
                           "CONTENT-TYPE: text/xml charset=\"utf-8\"\r\n"
                           "DATE: %s\r\n"
                           "EXT:\r\n"
                           "SERVER: Unspecified, UPnP/1.0, Unspecified\r\n"
                           "X-User-Agent: redsonic\r\n"
                           "CONNECTION: close\r\n"
                           "\r\n"
                           "%s" % (len(soap), date_str, soap))
                socket.send(message)
        else:
            dbg(data)

    def on(self):
        return False

    def off(self):
        return True


# Since we have a single process managing several virtual UPnP devices,
# we only need a single listener for UPnP broadcasts. When a matching
# search is received, it causes each device instance to respond.
#
# Note that this is currently hard-coded to recognize only the search
# from the Amazon Echo for WeMo devices. In particular, it does not
# support the more common root device general search. The Echo
# doesn't search for root devices.

class upnp_broadcast_responder(object):
    TIMEOUT = 0

    def __init__(self):
        self.devices = []

    def init_socket(self):
        ok = True
        self.ip = '239.255.255.250'
        self.port = 1900
        try:
            #This is needed to join a multicast group
            self.mreq = struct.pack("4sl",socket.inet_aton(self.ip),socket.INADDR_ANY)

            #Set up server socket
            self.ssock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
            self.ssock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

            try:
                self.ssock.bind(('',self.port))
            except Exception, e:
                dbg("WARNING: Failed to bind %s:%d: %s" , (self.ip,self.port,e))
                ok = False

            try:
                self.ssock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,self.mreq)
            except Exception, e:
                dbg('WARNING: Failed to join multicast group:',e)
                ok = False

        except Exception, e:
            dbg("Failed to initialize UPnP sockets:",e)
            return False
        if ok:
            dbg("Listening for UPnP broadcasts")

    def fileno(self):
        return self.ssock.fileno()

    def do_read(self, fileno):
        data, sender = self.recvfrom(1024)
        if data:
            if data.find('M-SEARCH') == 0 and data.find('urn:Belkin:device:**') != -1:
                for device in self.devices:
                    time.sleep(0.5)
                    device.respond_to_search(sender, 'urn:Belkin:device:**')
            else:
                pass

    #Receive network data
    def recvfrom(self,size):
        if self.TIMEOUT:
            self.ssock.setblocking(0)
            ready = select.select([self.ssock], [], [], self.TIMEOUT)[0]
        else:
            self.ssock.setblocking(1)
            ready = True

        try:
            if ready:
                return self.ssock.recvfrom(size)
            else:
                return False, False
        except Exception, e:
            dbg(e)
            return False, False

    def add_device(self, device):
        self.devices.append(device)
        dbg("UPnP broadcast listener: new device registered")


# This is an example handler class. The fauxmo class expects handlers to be
# instances of objects that have on() and off() methods that return True
# on success and False otherwise.
#
# This example class takes two full URLs that should be requested when an on
# and off command are invoked respectively. It ignores any return data.

class dummy_handler(object):
    def __init__(self, name):
        self.name = name

    def on(self):
        print self.name, "ON"
        return True

    def off(self):
        print self.name, "OFF"
        return True


class rest_api_handler(object):
    def __init__(self, on_cmd, off_cmd):
        self.on_cmd = on_cmd
        self.off_cmd = off_cmd

    def on(self):
        r = requests.get(self.on_cmd)
        return r.status_code == 200

    def off(self):
        r = requests.get(self.off_cmd)
        return r.status_code == 200

if __name__ == "__main__":
    FAUXMOS = [
        ['office lights', dummy_handler("officelight")],
        ['kitchen lights', dummy_handler("kitchenlight")],
    ]

    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        DEBUG = True

    # Set up our singleton for polling the sockets for data ready
    p = poller()

    # Set up our singleton listener for UPnP broadcasts
    u = upnp_broadcast_responder()
    u.init_socket()

    # Add the UPnP broadcast listener to the poller so we can respond
    # when a broadcast is received.
    p.add(u)

    # Create our FauxMo virtual switch devices
    for one_faux in FAUXMOS:
        switch = fauxmo(one_faux[0], u, p, None, 0, action_handler = one_faux[1])

    dbg("Entering main loop\n")

    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            dbg(e)
            break
