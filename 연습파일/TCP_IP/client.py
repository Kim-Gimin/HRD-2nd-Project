import socket

host = '127.0.0.1'
port = 9999

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# 게임 규칙 출력
print("0과 9 사이의 서로 다른 숫자 3개를 입력하세요.")

while True:
    # 숫자 입력 받기
    guess = input("숫자 3개를 하나씩 차례대로 입력하세요: ")
    # 입력된 숫자를 서버로 전송
    client_socket.send(guess.encode())

    # 서버로부터 정답 받기
    answer = client_socket.recv(1024).decode()
    # 정답 출력
    print("서버에서 받은 정답:", answer)

    # 정답을 맞췄으면 게임 종료
    if "축하합니다" in answer:
        break

# 연결 종료
client_socket.close()
