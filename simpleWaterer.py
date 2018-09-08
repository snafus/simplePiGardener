#!/usr/bin/env python

from __future__ import print_function
import sys, os, time
from datetime import datetime
import logging
from contextlib import contextmanager

import argparse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logger.error("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

logger.debug("GPIO VERSION: " + str(GPIO.VERSION))
logger.debug("GPIO INFO   : " + str(GPIO.RPI_INFO))



#GPIO.setup(pin_relay1, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(pin_relay2, GPIO.OUT, initial=GPIO.HIGH)
#
#state1 = GPIO.HIGH
#while True:
#    state1 = GPIO.HIGH if state1 != GPIO.HIGH else GPIO.LOW
#    GPIO.output(pin_relay1,state1)
#    if state1 == GPIO.HIGH:
#        time.sleep(10)
#    else:
#        time.sleep(3)

# GPIO.setup(channel, GPIO.IN)
# GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.input(channel)
# GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.output(channel, state)


class Relay(object):
    def __init__(self,gpio_pin,active_low=True):
        self._gpio_pin    = gpio_pin
        self._active_low = active_low
        self.ON  = GPIO.LOW  if self._active_low else GPIO.LOW
        self.OFF = GPIO.HIGH if self._active_low else GPIO.HIGH
        self._state = self.OFF
        GPIO.setup(gpio_pin, GPIO.OUT, initial=self.OFF)

    def switch_on(self):
        logger.debug("%r switch_on" % (self))
        GPIO.output(self._gpio_pin,self.ON)
        self._state = self.ON
    
    def switch_off(self):
        logger.debug("%r switch_off" % (self))
        GPIO.output(self._gpio_pin,self.OFF)
        self._state = self.OFF

    def toggle(self):
        if self._state == self.ON:
            self.switch_off()
        else:
            self.switch_on()

    def get_pin(self):
        return self._gpio_pin

    def get_state(self):
        """Note; returns LOW or HIGH; which does note 
        necessarily correspond to ON or OFF"""
        return self._state

    def get_status(self):
        if self._state == self.ON:
            return "ON"
        else:
            return "OFF"
    def is_on(self):
        return self._state == self.ON
    def is_off(self):
        return self._state == self.OFF

    def __str__(self):
        return "Relay {}: {}".format(self._gpio_pin, self.get_status())

    @contextmanager
    def safe_on(self):
        """For use with 'with' statements say.
        turn on the relay, yield (e.g. to sleep),
        and switch off, even on error, or interupt.
        """
        logger.debug("%r safe_on" % (self))
        try:
            self.switch_on()
            yield
        finally:
            self.switch_off()




#def main(argv):
#    GPIO.setmode(GPIO.BCM)
#
#    pin_relay1 = 17
#    pin_relay2 = 18
#
#    GPIO.setup(pin_relay1, GPIO.OUT, initial=GPIO.HIGH)
#    GPIO.setup(pin_relay2, GPIO.OUT, initial=GPIO.HIGH)
#    if int(argv[1]) == 1:
#        GPIO.output(pin_relay1,GPIO.LOW)
#    elif int(argv[1]) == 0:
#        GPIO.output(pin_relay1,GPIO.HIGH)

def test1(on_time,relay):
    logger.debug("Logger ontime: {:.1f}".format(on_time))

    print("{}: {}".format(str(datetime.now()),str(relay)))
    with relay.safe_on():
        print("{}: {}".format(str(datetime.now()),str(relay)))
        time.sleep(on_time)
    print("{}: {}".format(str(datetime.now()),str(relay)))


def trun():
    with relay_dummy.safe_on():
        print(relay_dummy)
        time.sleep(5)
    

def test2():
    GPIO.setmode(GPIO.BCM)
    relay_pump  = Relay(17,active_low=True)
    relay_dummy = Relay(18,active_low=True)

    from threading import Thread,Timer

    
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--ontime',dest='on_time', default=5., 
                    type=float,  help="Relay on time in integer seconds")
parser.add_argument('--delay',dest='delay', default=0., 
                    type=float,  help="delay on time in integer seconds")
parser.add_argument('--relay',dest='relay',default='pump',type=str,
                    help='Choice of relay [pump|dummy]')


if __name__ == '__main__':
    args = parser.parse_args()
    time.sleep(args.delay)
    GPIO.setmode(GPIO.BCM)
    relay_pump  = Relay(17,active_low=True)
    relay_dummy = Relay(18,active_low=True)
    
    test1(args.on_time,relay_pump if args.relay=='pump' else relay_dummy)


#relay_dummy.switch_on()



    #main(sys.argv)
    #time.sleep(float(sys.argv[2]))
    #main(['dummy',0])
    #GPIO.cleanup()





