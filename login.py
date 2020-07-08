import json  # json 모듈 불러오기
import getpass

path = './userinfo.json'


def json_write(data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def json_read():
    with open(path, 'r', encoding='UTF8') as f:
        # load, loads는 multiple value를 불러오지 못함. 따라서 하나의 list안에 정리.
        userinfo_data = json.load(f)
    return userinfo_data


def json_append(path, data):
    with open(path, 'a') as f:
        json.dump(data, f, indent=4)


def main():
    while True:
        pick = input("로그인 하시려면 1번, 회원가입을 하시려면 2번을 눌러주세요.")
        if pick == '1':
            login()
            return
        elif pick == '2':
            signup()
            login()
            return
        else:
            print("다시 입력해주세요.")


def signup():
    userdata = json_read()
    tempdict = {
        "id": "",
        "password": "",
        "name": "",
        "age": "",
        "job": "",
    }


    tempdict['id'] = checkid()
    tempdict['password'] = checkpw()
    tempname = input("이름을 입력해주세요: ")
    tempdict['name'] = tempname
    
    while True:
        tempjob = input("학생은 1번, 선생님은 2번을 입력해주세요: ")
        if tempjob=='1':
            tempdict['job'] = '학생'
            tempdict['age'] = checkage()
            tempfeel = input("앞으로 5개월동안의 다짐을 입력해주세요: ")
            tempdict['feeling'] = tempfeel
            tempint = input("관심사를 입력해주세요: ")
            tempdict['interest'] = tempint
            userdata['students'].append(tempdict)
            break
        if tempjob=='2':
            tempdict['job'] = '선생님'
            tempdict['age'] = input("나이를 입력해주세요:")
            userdata['teachers'].append(tempdict)
            break
        else:
            continue
    
    json_write(userdata)
    return


def checkid():
    while True:
        tempid = input("아이디를 입력해주세요: ").lower()
        if tempid == None:
            continue
        if len(tempid) > 12:
            print('12자 이하로 입력해주세요.')
            continue
        else:
            for i in range(len(tempid)):
                if tempid[i].isalpha is False:
                    print("소문자만 입력해주세요.")
                    continue
                else:
                    return tempid


def checkpw():
    while True:
        temppw = getpass.getpass("패스워드를 입력하세요: ")
        if len(temppw) > 12:
            print("12자 이하로 입력해주세요.")
            continue
        pwcheck = getpass.getpass("패스워드를 한번 더 입력하세요: ")
        if temppw != pwcheck:
            print("비밀번호가 다릅니다.")
            continue
        else:
            return temppw

def checkage():  #20살 미만만 입력받기
    while True:
        tempage = input("나이를 입력해주세요:")
        if int(tempage)<=0:
            continue
        elif int(tempage)>=20:
            print('20살 이상입니다.')
            continue
        else:
            return tempage


    


def login():
    print("==========================로그인 창입니다=========================")
    while True:
        userid = input("아이디를 입력하세요")
        pw = getpass.getpass("패스워드를 입력하세요")

        userdata = json_read()

        for user in userdata['students']:
            if userid == user['id'] and pw == user['password']:
                print("로그인 되었습니다.")
                after_login(userid)
                return

        for user in userdata['teachers']:
            if userid == user['id'] and pw == user['password']:
                print("로그인 되었습니다.")
                after_login(userid)
                return

        print("아이디 혹은 비밀번호가 잘못되었거나 없는 사용자입니다. 다시 시도하세요.")

    return


def after_login(my_id):
    myid = my_id
    users = json_read()

    for idx, user in enumerate(users['students']):
        if user['id'] == myid:
            myinfo = user
            del users['students'][int(idx)]
            otheruser_students = users['students']
    
    for idx, user in enumerate(users['teachers']):
        if user['id'] == myid:
            myinfo = user
            del users['teachers'][int(idx)]
            otheruser_teachers = users['teachers']

    while True:
        x = input(
            "\n1.마이페이지 보기\n2.다른 유저 보기\n3.추가 기능\n4.종료하기\n\n원하는 항목의 번호를 입력하세요: ")
        if x == '1':
            print(f'{myinfo}')

        if x == '2':
            for idx, user in enumerate(otheruser_students):
                print(idx, user['id'])
            while(True):
                y = input("정보를 보고싶은 회원의 번호를 입력하세요: ")
                if int(y) < 0 or int(y) >= len(otheruser_students):
                    print("존재하지 않는 회원번호입니다.")
                    continue
                print(otheruser_students[int(y)])
                z = input("다른 회원의 정보를 보시려면 0, 메뉴로 돌아가시려면 1을 입력하세요:")
                if z == '1':
                    break
                if z == '0':
                    continue

        if x == '3':
            additionalfunc()
            continue

        if x == '4':
            break
        else:
            continue

    return


def print_all_student_name():
    users = json_read()
    for student in users['students']:
        print(student['name'])
    return


def print_under_20():
    users = json_read()
    i=0
    for student in users['students']:
        if int(student['age']) < 20:
            print(student['name'])
            i=i+1
    if i==0:
        print("모든 학생이 성인입니다.")
    return


def additionalfunc():
    while True:
        x = input("\n1.학생 이름 전부 출력하기\n2.성인이 아닌 학생 출력하기\n3.이전으로 돌아가기\n\n원하는 항목의 번호를 입력하세요: ")

        if x == '1':
            print('\n')
            print_all_student_name()
            continue
        if x == '2':
            print('\n')
            print_under_20()
            continue
        if x == '3':
            break
    
    return


main()
