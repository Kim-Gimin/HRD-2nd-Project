import socket
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
leds = [23, 24, 25, 1]
for i in leds:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

HOST = 'localhost'
PORT = 9999

def handle_client(client_socket, client_address):
    answer = [random.randint(1, 9) for _ in range(3)]
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
            client_socket.send(message.encode("utf-8"))

            if strikes == 3:
                client_socket.send(b"Congratulations, you guessed the correct numbers!\n")
                break
            else:
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
    print(f"[-] Closed connection from {client_address[0]}:{client_address[1]}")
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("[*] Listening on 0.0.0.0:9999")
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            break

    server_socket.close()

def run_client():
    server_host = "localhost"
    server_port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    while True:
        message = input("Guess the three numbers (separated by spaces): ")
        client_socket.send(message.encode("utf-8"))

        data = client_socket.recv(1024).decode("utf-8")
        print(data, end="")

        if "Congratulations" in data:
            break

    client_socket.close()


if __name__ == "__main__":
    run_client()
