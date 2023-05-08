import socket

def run_client():
    server_host = "localhost"
    server_port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # 서버에서 먼저 보내는 환영 메시지 출력
    data = client_socket.recv(1024).decode("utf-8")
    print(data, end='')

    while True:
        message = input("Guess the three numbers (separated by spaces): ")
        client_socket.send(message.encode("utf-8"))

        data = client_socket.recv(1024).decode("utf-8")
        print(data, end='')

        if "Congratulations" in data:
            break

    client_socket.close()


if __name__ == "__main__":
    run_client()
