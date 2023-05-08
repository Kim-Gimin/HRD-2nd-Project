import socket
from random import randint

def generate_numbers():
    numbers = []
    while len(numbers) < 3:
        new_number = randint(0, 9)
        if new_number not in numbers:
            numbers.append(new_number)
    return numbers

def get_score(guess, solution):
    strike_count = 0
    ball_count = 0
    i = 0

    while i < len(guess):
        if guess[i] == solution[i]:
            strike_count += 1
        elif guess[i] in solution:
            ball_count += 1
        i += 1

    return strike_count, ball_count

def play_game(client_socket):
    answer = generate_numbers()
    print("Answer:", answer)

    while True:
        # 클라이언트로부터 데이터를 받습니다.
        data = client_socket.recv(1024)
        if not data:
            # 클라이언트가 연결을 끊은 경우
            break

        guess = [int(d) for d in data.decode().strip()]
        print("Guess:", guess)

        # 점수 계산
        strike, ball = get_score(guess, answer)

        # 결과를 클라이언트에게 보냅니다.
        client_socket.sendall(f"{strike}S{ball}B\n".encode())

        # 정답을 맞춘 경우
        if strike == 3:
            break

    client_socket.close()

if __name__ == '__main__':
    # 서버 소켓을 생성합니다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 로컬 호스트의 포트 12345를 사용합니다.
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # 클라이언트의 접속을 대기합니다.
    server_socket.listen(1)
    print("Waiting for client connection...")

    # 클라이언트의 접속이 되면 게임을 시작합니다.
    client_socket, client_address = server_socket.accept()
    print("Connected by", client_address)

    play_game(client_socket)

    # 서버 소켓을 닫습니다.
    server_socket.close()
