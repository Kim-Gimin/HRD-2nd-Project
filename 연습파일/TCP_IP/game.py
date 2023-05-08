import socket
import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [23, 24, 25, 1]
for i in leds:
    GPIO.setup(i, GPIO.OUT)
HOST = 'localhost'
PORT = 9999
send_message:str = ''

Strikes = 0
Balls = 0

def sending_message(sock):
    while True:
        if not str(Strikes == 0 and Balls == 0):
            received_message(sock, Strikes, Balls)
        if GPIO.input(leds[0]):
            pass
        elif GPIO.input(leds[1]):
            pass
        
def received_message(sock, s=0, b=0):
    data = sock.recv(1024).decode(encoding = 'utf-8')
    data = data.strip()
    GPIO.output(leds[0], GPIO.LOW)
    GPIO.output(leds[1], GPIO.LOW)
    GPIO.output(leds[2], GPIO.LOW)
    GPIO.output(leds[3], GPIO.LOW)
    
    if data == str(s == 0 and b == 0):
        pass
    elif data == str(s == 0 and b == 1):
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(s == 0 and b == 2):
        GPIO.output(leds[2], GPIO.HIGH)
        pass
    elif data == str(s == 0 and b == 3):
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(s == 1 and b == 0):
        GPIO.output(leds[1], GPIO.HIGH)
        pass
    elif data == str(s == 1 and b == 1):
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(s == 1 and b == 2):
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        pass
    elif data == str(s == 2 and b == 0):
        GPIO.output(leds[0], GPIO.HIGH)
        pass
    elif data == str(s == 2 and b == 1):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(s == 3 and b == 0):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass


    data = sock.recv(1024).decode(encoding = 'utf-8')
    data = data.strip()
    GPIO.output(leds[0], GPIO.LOW)
    GPIO.output(leds[1], GPIO.LOW)
    GPIO.output(leds[2], GPIO.LOW)
    GPIO.output(leds[3], GPIO.LOW)
    
    if data == str(Strikes == 0 and Balls == 0):
        pass
    elif data == str(Strikes == 0 and Balls == 1):
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(Strikes == 0 and Balls == 2):
        GPIO.output(leds[2], GPIO.HIGH)
        pass
    elif data == str(Strikes == 0 and Balls == 3):
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(Strikes == 1 and Balls == 0):
        GPIO.output(leds[1], GPIO.HIGH)
        pass
    elif data == str(Strikes == 1 and Balls == 1):
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(Strikes == 1 and Balls == 2):
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        pass
    elif data == str(Strikes == 2 and Balls == 0):
        GPIO.output(leds[0], GPIO.HIGH)
        pass
    elif data == str(Strikes == 2 and Balls == 1):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass
    elif data == str(Strikes == 3 and Balls == 0):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        pass


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as sock:
    try:
        sock.connect((HOST, PORT))
        t1 = threading.Thread(target=sending_message, args=(sock,))
        t2 = threading.Thread(target=received_message, args=(sock, Strikes, Balls))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()
