import socket
import random
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # warning 끄기
leds = [23, 24, 25, 1]
for i in leds:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

HOST = 'localhost'
PORT = 9999
