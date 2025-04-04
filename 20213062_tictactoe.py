import random

#이기는 경로
win_condition = []

#승리 데이터 크기
input_data = 100

#선공
turn1 = 'O'
#후공
turn2 = 'X'

def game_reset():
    game_cur = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    #게임 진행사항 저장
    big_data = []
    return game_cur, big_data

def game_moment(game_cur):
    print("==========게임  현황==========\n")
    for i in range(3):
        print("           ", end ="")
        for k in range(3):
            #열 만들기
            print(game_cur[i][k], end="")
            if k<2:
                print("||" ,end="")
        #행 끝남 표시:
        if i<2:
            print("\n           ", end ="")
            print("ㅡ ㅡ ㅡ") 
    print("\n\n=============================")   

#big_data에서 확인
def check_data(big_data, win_condition, start, turn):
    while(1):
        if not win_condition:
            return 0
        else:
            if not big_data:
                return 0
            else:
                correct_list = []
                for i in range(len(win_condition)): 
                    if len(big_data) <= start:
                        return 0
                    else:
                        #print(big_data[start])
                        #print(win_condition[i][start])
                        if(big_data[start]==win_condition[i][start]):
                            if turn == turn2:
                                if len(win_condition[i])%2==0:
                                    correct_list.append(win_condition[i])  
                                else:
                                    continue
                            elif turn == turn1:
                                if len(win_condition[i])%2==1: 
                                    correct_list.append(win_condition[i])
                                else:
                                    continue
                        else:
                            continue
                win_condition = correct_list  
                print('승리 조건', win_condition)
                start += 1
                print('비교',start, len(big_data))
                if not win_condition:
                    return 0
                elif start < (len(big_data)):
                    continue
                else: 
                    num = random.choice(list(range(0, len(win_condition))))
                    com_result = win_condition[num][len(big_data)]
                    print("선택한 경로",win_condition[num])
                    print(big_data)
                    return com_result

#처음부터 컴퓨터 차례까지 일치하는 것 중에 2개 이상이라면 랜덤으로 실행 -> 어짜피 어떤 것이든 승리로 가는 길들이기 때문에

def alpa_toe(game_cur, big_data, win_condition, turn):
    next_step = check_data(big_data, win_condition, 0, turn)
    if next_step != 0:
        #경험했던 코스라면 코스를 따라 진행
        print('next step', next_step)
        if next_step[0] == turn:
            game_cur[int(next_step[2])][int(next_step[1])] = turn
            big_data.append(turn + str(int(next_step[1]))+str(int(next_step[2])))
    else:
        #경험했던 방식이 아니라면 랜덤으로 진행
        remainder = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        while(1):
            if not remainder:
                #승자 없이 끝남
                print("There is no winner\n")
                return 1
            else:
                #게임이 끝나지 않았으면 랜덤으로 실행
                num = int(random.choice(remainder))
                #이미 선택한 자리를 랜덤이 고른다면 제외하고 다시 실행
                if (game_cur[int(num//3)][int(num%3)] == 'O' or game_cur[int(num//3)][int(num%3)] == 'X'):
                    remainder.remove(num)
                    continue
                #랜덤으로 비어있는 곳을 'X'표시함
                else:
                    print("random choose")
                    game_cur[int(num//3)][int(num%3)] = turn
                    big_data.append(turn + str(int(num%3))+str(int(num//3)))
                    break

def readWinner(array,target):
    #2차원 배열을 1차원 배열로
    q=0
    a=sum(array,[])
    for i in range(3):
        # 가로 체크
        if a[0 + i * 3] == target and a[1 + i * 3] == target and a[2 + i * 3] == target:
            return 1
        # 세로 체크
        if a[i] == target and a[i + 3] == target and a[i + 6] == target:
            return 1
    # \
    if a[0] == target and a[4] == target and a[8] == target: 
        return 1
    # /
    if a[2] == target and a[4] == target and a[6] == target:
        return 1
    
    return 0

def first_main_system():
    game_cur, big_data = game_reset()
    while(' ' in game_cur[0] or ' ' in game_cur[1] or ' ' in game_cur[2]):
        game_moment(game_cur)

        A_choice = input("선택하실 좌표를 입력하세요 (x,y) : ")
        if (int(A_choice[0]) > 3 or int(A_choice[2])>3):
            print("0, 1, 2 중 선택해주세요")
            continue
        elif(game_cur[int(A_choice[2])][int(A_choice[0])] == 'O' or game_cur[int(A_choice[2])][int(A_choice[0])]=='X'):
            print("이미 선택된 자리입니다.")
            continue
        else:
            game_cur[int(A_choice[2])][int(A_choice[0])] = turn1
            big_data.append(turn1+str(A_choice[0]) + str(A_choice[2]))
            
        #승패 결정
        if readWinner(game_cur, turn1):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already win condition")
                
            game_moment(game_cur)
            print("first player is the winner")
            break
        else:
            game_moment(game_cur)
        
        #컴퓨터 선택
        alpa_toe(game_cur, big_data, win_condition, turn2)
        if readWinner(game_cur, turn2):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already win condition")
            game_moment(game_cur)
            print("second player is the winner")
            break
        else:
            game_moment(game_cur)

def second_main_system():
    game_cur, big_data = game_reset()
    while(' ' in game_cur[0] or ' ' in game_cur[1] or ' ' in game_cur[2]):
        game_moment(game_cur)

        #컴퓨터 선택
        alpa_toe(game_cur, big_data, win_condition, turn1)
        if readWinner(game_cur, turn1):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already be in win condition")
            game_moment(game_cur)
            print("first player is the winner")
            break
        else:
            game_moment(game_cur)

        #플레이어 차례
        A_choice = input("선택하실 좌표를 입력하세요 (x,y) : ")
        if (int(A_choice[0]) > 3 or int(A_choice[2])>3):
            print("0, 1, 2 중 선택해주세요")
            continue
        elif(game_cur[int(A_choice[2])][int(A_choice[0])] == 'O' or game_cur[int(A_choice[2])][int(A_choice[0])]=='X'):
            print("이미 선택된 자리입니다.")
            continue
        else:
            game_cur[int(A_choice[2])][int(A_choice[0])] = turn2
            big_data.append(turn2+str(A_choice[0])+str(A_choice[2]))

        #승패 결정
        if readWinner(game_cur, turn2):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already be in win condition")
            game_moment(game_cur)
            print("second player is the winner")
            break
        else:
            game_moment(game_cur)
        
def com_main_system():
    game_cur, big_data = game_reset()
    gam1 = 0
    gam2 =0
    while(' ' in game_cur[0] or ' ' in game_cur[1] or ' ' in game_cur[2]):
        game_moment(game_cur)

        #컴퓨터1의 선택
        alpa_toe(game_cur, big_data, win_condition, turn1)
        #승자 있는지 체크
        if readWinner(game_cur, turn1):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already win condition")
                gam1 += 1
            game_moment(game_cur)
            print("first player is the winner")
            break
        else:
            game_moment(game_cur)
        
        #컴퓨터2의 선택
        alpa_toe(game_cur, big_data, win_condition, turn2)
        if readWinner(game_cur, turn2):
            #목록 추가 후 종료
            if big_data not in win_condition:
                win_condition.append(big_data)
            else:
                print("already win condition")
                gam2 += 1
            game_moment(game_cur)
            print("second player is the winner")
            break
        else:
            game_moment(game_cur)

def main_system():
    response = input("게임을 시작하시겠습니까? (yes or no) : ")
    while(response == 'yes'):
        start = input("먼저 하시겠습니까? (yes or no) : ")
        if start == 'yes':
            first_main_system()
        elif start == 'no':
            second_main_system()
        elif start == 'com':
            data_count = 0
            while(data_count!=input_data):
                data_count += 1
                com_main_system()
                print("반복횟수 : ", data_count, "// 승리 데이터 : ", win_condition)
        else:
            print("잘못 입력하셨습니다.")
            continue
        response = input("게임을 다시 시작하시겠습니까? (yes or no) : " )
    print("게임을 종료합니다.")

if __name__=="__main__":
    game_reset()
    main_system()
