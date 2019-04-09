#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

print()
print('Script startet:')
print()

GPIO.setwarnings(False)
# GPIO Bezeichnung anstelle von Pinnummer benutzen
GPIO.setmode(GPIO.BCM)

# GPIO 7-10 betrachteten Pins
pins = range(7, 11)

# Pins als Ausgaenge:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Alle LEDs werden auf aus gestellt
for pin in pins:
    GPIO.output(pin, GPIO.HIGH)


# LEDs werden angeschaltet
def led_anschalten(led_nr):
    GPIO.output(led_nr, GPIO.LOW)


# LEDS werden ausgeschaltet:
def led_ausschalten(led_nr):
    GPIO.output(led_nr, GPIO.HIGH)


# Zustand der LEDs wird gewechselt    
def toggle(led_nr):
    GPIO.output(led_nr, not GPIO.input(led_nr))



count = 0

while count < 60:
    count = count +1
    time.sleep(1)
    toggle(pins[0])
    if count % 2 == 0:
        toggle(pins[1])
    if count % 4 == 0:
        toggle(pins[2])
    if count % 8 == 0:
        toggle(pins[3])

GPIO.cleanup()
print('Script beendet.')
