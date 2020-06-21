#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
from gpiozero import CPUTemperature
import time
from datetime import datetime
from signal import *
import sys, time

def clean(*args):
    print("clean me")
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

#from demo_opts import get_device
from luma.core.render import canvas
from luma.core import cmdline, error
from PIL import ImageFont

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    #av1, av2, av3 = os.getloadavg()
    return "UpTime: %s" \
        % (str(uptime).split('.')[0])
    #return "Ld:%.1f %.1f %.1f Up: %s" \
    #    % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def cpuTemp():
    temp = CPUTemperature()
    return "CPU Temp: %.2f°C" \
        % (temp.temperature)
    #print(cpu.temperature)


def stats(device):
    # use custom font

    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)
    #font2 = ImageFont.load_default()

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 26), cpuTemp(), font=font2, fill= "white")
            draw.text((0, 38), disk_usage('/'), font=font2, fill="white")
            try:
                draw.text((0, 50), network('wlan0'), font=font2, fill="white")
            except KeyError:
                # no wifi enabled/available
                pass


def main():
    while True:
        stats(device)
        time.sleep(2)

class dispSettings:
    backlight_active='low'
    bgr=False
    block_orientation=0
    config=None
    display='sh1106'
    duration=0.01
    framebuffer='diff_to_previous'
    ftdi_device='ftdi://::/1'
    gpio=None
    gpio_backlight=18
    gpio_data_command=24
    gpio_mode=None
    gpio_reset=25
    h_offset=0
    height=64
    i2c_address='0x3C'
    i2c_port=1
    interface='spi'
    loop=0
    max_frames=None
    mode='RGB'
    rotate=0
    scale=2
    spi_bus_speed=8000000
    spi_cs_high=True
    spi_device=0
    spi_port=0
    spi_transfer_size=4096
    transform='scale2x'
    v_offset=0
    width=128


def get_device():
    """
    Create device from command-line arguments and return it.
    """
    args = dispSettings()

    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        print(e)

    return device

# State Machine using a Switch Case Workaround in Python
# Implement Python Switch Case Statement using Class
class StateMachine:

    def switchState(self, state):
        default = "Not a valid State"
        return getattr(self, 'state_' + state, lambda: default)()

    def state_Init(self):
        print("State Machine now in State 'Init'")
        time.sleep(2)
        self.switchState("1")
        print("State Machine automatically switching to State '1'")
 
    def state_1(self):
        print("State Machine now in State '1'")
        time.sleep(2)
        self.switchState("Init")
        print("State Machine automatically switching to State 'Init'")
 

s = StateMachine()

if __name__ == "__main__":
    try:
        device = get_device()

        main()
    except KeyboardInterrupt:
        pass


