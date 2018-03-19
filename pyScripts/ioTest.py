#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# GPIO Bezeichnung anstelle von Pinnummer benutzen
GPIO.setmode(GPIO.BCM)

# Bin 7-10 als Ausgang:
for pin_nr in range(7, 11):
    GPIO.setup(pin_nr, GPIO.OUT)


while True:
    for led_nr in range(7, 11):
        GPIO.output(led_nr, not GPIO.input(led_nr))
        time.sleep(0.5)
