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

# 스위치 핀 번호와 pull-up 설정
switch_pin = 4
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

HOST = 'localhost'
PORT = 9999
answer = [4, 5, 6]  # 정답을 고정시킴

# 남은 동전 수를 관리하는 함수
def manage_coins(remaining_coins):
    if remaining_coins == 0:
        print("YOU LOSE")
    elif remaining_coins == 1:
        print(f"LAST COIN: {remaining_coins}")
    else:
        print(f"REMAINING COINS: {remaining_coins}")

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("[*] Listening on 127.0.0.1:9999")

    # 초기 남은 동전 수를 10으로 설정
    remaining_coins = 10
    
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address, remaining_coins)
        except KeyboardInterrupt:
            break

    server_socket.close()

def handle_client(client_socket, client_address, remaining_coins):
    for i in leds:
        GPIO.output(i, GPIO.LOW)
    
    print(f"[+] New connection from {client_address[0]}:{client_address[1]}")
    client_socket.send(b"Welcome to the baseball game!\n")
    while True:
        try:
            data = client_socket.recv(1024).strip().decode("utf-8")
            if not data:
                break

            guess = list(map(int, data.split()))
            if len(guess) != 3:
                client_socket.send(b"Invalid input. Try again.\n")
                continue

            strikes, balls = 0, 0
            for i, num in enumerate(guess):
                if num == answer[i]:
                    strikes += 1
                elif num in answer:
                    balls += 1

            message = f"Strikes: {strikes}, Balls: {balls}\n"

            # 스위치가 눌렸는지 확인
            switch_state = GPIO.input(switch_pin)
            if switch_state == GPIO.LOW:  # 스위치가 눌렸을 때
                manage_coins(remaining_coins)  # 남은 동전 수 출력
                if remaining_coins <= 1:
                    client_socket.send(b"Game over. You lose!\n")
                    break
            else:
                if remaining_coins == 2:
                    client_socket.send(b"LAST COIN!\n")
                else:
                    remaining_coins -= 1
                    client_socket.send(f"REMAINING COINS: {remaining_coins}\n".encode())

              # 스위치가 눌리지 않았을 때
            client_socket.send(message.encode("utf-8"))

            if strikes == 3:
                client_socket.send(b"Congratulations, you guessed the correct numbers!\n")
                for i in range(3):
                    for led in leds:
                        GPIO.output(led, GPIO.HIGH)
                    time.sleep(0.2)
                    for led in leds:
                        GPIO.output(led, GPIO.LOW)
                    time.sleep(0.2)
                break

            else:
                for i in leds:
                    GPIO.output(i, GPIO.LOW)  # 매번 LED 초기화   
                if strikes == 0 and balls == 1:
                    GPIO.output(leds[3], GPIO.HIGH)
                elif strikes == 0 and balls == 2:
                    GPIO.output(leds[2], GPIO.HIGH)
                elif strikes == 0 and balls == 3:
                    GPIO.output(leds[2], GPIO.HIGH)
                    GPIO.output(leds[3], GPIO.HIGH)
                elif strikes == 1 and balls == 0:
                    GPIO.output(leds[1], GPIO.HIGH)
                elif strikes == 1 and balls == 1:
                    GPIO.output(leds[1], GPIO.HIGH)
                    GPIO.output(leds[3], GPIO.HIGH)
                elif strikes == 1 and balls == 2:
                    GPIO.output(leds[1], GPIO.HIGH)
                    GPIO.output(leds[2], GPIO.HIGH)
                elif strikes == 2 and balls == 0:
                    GPIO.output(leds[0], GPIO.HIGH)
                elif strikes == 2 and balls == 1:
                    GPIO.output(leds[0], GPIO.HIGH)
                    GPIO.output(leds[3], GPIO.HIGH)
            
        except Exception as e:
            print(f"[x] Error: {e}")
            break

    client_socket.close()
    for i in leds:
        GPIO.output(i, GPIO.LOW)
    print(f"[-] Closed connection from {client_address[0]}:{client_address[1]}")

if __name__ == "__main__":
    run_server()
