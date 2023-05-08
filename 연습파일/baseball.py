from random import randint


def generate_numbers():
    numbers = [3,4,5]
    #i = 0
    #new_number = 0
    #while i < 3:
    #    new_number = randint(0, 9)
    #    if new_number not in numbers:
    #        numbers.append(new_number)
    #        i += 1
    print("0과 9 사이의 서로 다른 숫자 3개를 랜덤한 순서로 뽑았습니다.\n")
    return numbers


def take_guess():
    print("숫자 3개를 하나씩 차례대로 입력하세요.")
    i = 0
    new_guess = []
    while i < 3:
        gue_number = int(input("{}번째 숫자를 입력하세요: ".format(i + 1)))
        if gue_number > 9:
            print("범위를 벗어나는 숫자입니다. 다시 입력하세요.")
            continue
        if gue_number in new_guess:
            print("중복되는 숫자입니다. 다시 입력하세요. ")
        else:
            new_guess.append(gue_number)
            i += 1

    return new_guess


def get_score(guess, solution):
    strike_count = 0
    ball_count = 0
    i = 0

    while i < len(guess):
        if guess[i] == solution[i]:
            strike_count += 1
            i += 1
        elif guess[i] in solution:
            ball_count += 1
            i += 1
        else:
            i += 1

    return strike_count, ball_count


# 여기서부터 게임 시작!
ANSWER = generate_numbers()
tries = 0

while 1:
    GUESS = take_guess()
    strike, ball = get_score(GUESS, ANSWER)
    print("{}S {}B ".format(strike, ball))

    if strike == 3:
        tries += 1
        break
    else:
        tries += 1

print("축하합니다. {}번 만에 숫자 3개의 값과 위치를 모두 맞추셨습니다.".format(tries))
