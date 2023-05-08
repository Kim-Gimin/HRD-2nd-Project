import socket
import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [23, 24, 25, 1]
for i in leds:
    GPIO.setup(i, GPIO.OUT)
    pass
HOST = 'localhost'
PORT = 9999

send_message:str = ''

def sending_message(clnt):
    while True:
        if GPIO.input(leds[0]):
            pass
        #send_message = 'LED 1 LIGHIT ON that is checked'
        #clnt.sendall(send_message.encode(encoding='utf-8'))
        elif GPIO.input(leds[1]):
            pass
        #send_message = 'LED 2 LIGHIT ON that is checked'
        #clnt.sendall(send_message.encode(encoding='utf-8'))

def received_message(clnt):
    while True:
        data = clnt.recv(1024).decode(encoding = 'utf-8')
        data = data.strip()
        if data == 'led1_on':
            GPIO.output(leds[0], GPIO.HIGH)
            print('LED 1 ON')
            pass
        elif data == 'led1_off':
            GPIO.output(leds[0], GPIO.LOW)
            print('LED 1 OFF')
            pass
        elif data == 'led2_on':
            GPIO.output(leds[1], GPIO.HIGH)
            print('LED 2 ON')
            pass
        elif data == 'led2_off':
            GPIO.output(leds[1], GPIO.LOW)
            print('LED 2 OFF')
            pass
        elif data == 'all_led_off':
            GPIO.output(leds[0], GPIO.LOW)
            GPIO.output(leds[1], GPIO.LOW)
            print('LED1, LED2 OFF')
            pass
        elif data == 'all_led_on':
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[1], GPIO.HIGH)
            print('LED1, LED2 ON')
            pass
        #print(data)

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as clnt:
    try:
        clnt.connect((HOST, PORT))
        t1 = threading.Thread(target=sending_message, args=(clnt,))
        t2 = threading.Thread(target=received_message, args=(clnt,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Keybpard interrupt")
    finally:
        GPIO.cleanup()

