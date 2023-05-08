import socket
import time
import RPi.GPIO as GPIO

def run_client():
    server_host = "localhost"
    server_port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # 서버에서 먼저 보내는 환영 메시지 출력
    data = client_socket.recv(1024).decode("utf-8")
    print(data, end='')

    remaining_coins = 10
    while remaining_coins > 0:
        message = input("Guess the three numbers (separated by spaces): ")
        client_socket.send(message.encode("utf-8"))

        data = client_socket.recv(1024).decode("utf-8")

        # 스위치가 눌렸는지 확인
        switch_state = GPIO.input(switch_pin)
        if switch_state == GPIO.LOW:  # 스위치가 눌렸을 때
            if remaining_coins == 1:
                print(f"LAST COIN: {remaining_coins}")
            else:
                print(f"REMAINING COINS: {remaining_coins}")
        else:  # 스위치가 눌리지 않았을 때
            print(data, end='')

            if "Congratulations" in data:
                break
            elif "Invalid" in data:
                continue

            remaining_coins -= 1
            if remaining_coins == 0:
                print("YOU LOSE")
                break

    client_socket.close()

if __name__ == "__main__":
    # 핀 번호 표기법 지정
    GPIO.setmode(GPIO.BCM)

    # 스위치 핀 번호와 pull-up 설정
    switch_pin = 4
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    run_client()
