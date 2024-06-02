from flask import Flask, request, redirect, render_template, url_for, session
from modules.flex import login_system
from env import FLASK_ENUM, SQL, SEND, HCAPTCHA
from modules.friends import friend_system
from modules.timetable import time_table_system
from modules.matchtime import matchsystem
import json
from src.lib import message, storage
from flask_hcaptcha import hCaptcha 
from modules.timeline import time_checker
import random

app = Flask(__name__, static_url_path='/static')
app.secret_key = FLASK_ENUM.SECRET_KEY

app.config['HCAPTCHA_ENABLED'] = True # 활성화 여부 (BOOL)
app.config['HCAPTCHA_SITE_KEY'] = HCAPTCHA.HCAPTCHA_SITE_KEY # 사이트 키 (SITE KEY)
app.config['HCAPTCHA_SECRET_KEY'] = HCAPTCHA.HCAPTCHA_SECRET_KEY# 시크릿 키 (SECRET KEY)
hcaptcha = hCaptcha(app) # 셋업
random_numbers = random.sample(range(1,20),15)
list = time_checker()
time_table_list = list.time_list()


@app.route('/login', methods=['GET','POST'])
def login():
    
    next = '로그인이 필요합니다.'
    if request.method == 'POST': 
        kras_login_system = login_system() 
        friend_system_data = friend_system.recommend(None)
        id = request.form.get('id') 
        password = request.form.get('password') 
        print(id, password)  
        random_numbers = random.sample(range(1,20),15)


        auth_inform = kras_login_system.new_login(id, password)

    
        print(random_numbers)

        print("정보")
        print(auth_inform)
        if auth_inform :
            next = '로그인성공'
            session["username"] = auth_inform[0] #세션에 저장
            session["userid"] = auth_inform[0][1]
            print(next)
            return render_template('main.html', state = next, user = auth_inform[0][0],recommend_friend = friend_system_data, time_table_list=time_table_list,k=random_numbers)
        
        else:
            status_code = "password_incorrect"
            return render_template('login.html',status_code = status_code)
    
    return render_template('login.html') 

@app.route('/friendrecommend')
def friendrecommend():
    friend_system_data = friend_system.recommend(None)
    print("데이터",friend_system_data)
    return render_template('index.html',recommend_friend = friend_system_data, k=random_numbers,)

@app.route('/timetable',methods=['POST'])
def timetable():
    user = session.get('username')[1]
    print('session',user)
    kras_timetable_system = time_table_system()
    timetable_data = kras_timetable_system.table_data(user)[0]
    print(timetable_data)
    #유저개인페이지
    return render_template('time_table.html',user=user,data=timetable_data)
    
@app.route('/matchtime',methods=['POST'])
def matchtime():
    user = session.get('username')[1]
    kras_timetable_system = time_table_system()
    timetable_data = kras_timetable_system.table_data(user)[0]
    rest_time = kras_timetable_system.table_data(user)[1]
    another_user = matchsystem()
    print("User의 잔여시간",rest_time)
    target_user = another_user.search_friend()
    print("상대방의 잔여시간",target_user[1][1])

    tmp_data = []
    target = target_user[1][1]

    for i in range(5):
        s1 = rest_time[i]
        s2 = target[i]
        
        print(s1,s2)
        
        result = set(s1) & set(s2)
        tmp_data.append(result)

    print(f"교집합{i}", tmp_data)

    day = ["월요일","화요일","수요일","목요일","금요일"]

    return render_template('time_table.html',user=user,data=timetable_data,schedule=tmp_data,day=day)

@app.route('/fix',methods=['GET','POST'])
def fix():

    if request.method == 'POST':
        data = request.form.get('data')
    
    print(data)

    
    user = session.get('username')[1]
    print("사용자",user)
    phone_num = matchsystem()
    send_number = phone_num.phone_num(user)
    numbers = ''.join(filter(str.isdigit, send_number[0]))

    
    print(numbers)
    
    data = {
            'messages': [
                {
                    'to': numbers,
                    'from': SEND.SENDNUMBER,
                    'subject': 'KRAS-약속 확정안내',
                    'text': f'안녕하세요 :) \n<{data}> 약속이 확정되었습니다. \n서비스를 이용해주셔서 감사합니다.\nActiveJang'
                }
            ]
        }
        
    res = message.send_many(data)
    print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
    
    return '전송완료'

@app.route('/main')
def loading_spinner():
    return render_template('loading_spinner.html')


@app.route('/redirect', methods = ['POST'])
#메인에서 바로 접속하면 오류가 발생하여, 한번 거치고 접근.
def goto_redirect():
    #return redirect(url_for('login'))
    return render_template('render.html')

@app.route('/main', methods=['POST'])
def main():
    next = '로그인성공'
    user = session.get('username')
    random_numbers = random.sample(range(1,20),15)
  
    print(random_numbers)
    friend_system_data = friend_system.recommend(None)
    if "username" in session: 
        return render_template('main.html',state = next, k=random_numbers)
    else:
        return render_template('login.html')

@app.route('/lightning_meet', methods = ['POST'])
def lightning_meet():
    return render_template('lightning_meet.html')

@app.route('/regular_meet', methods = ['POST'])
def regular_meet():
    return render_template('regular_meet.html')

@app.route('/friend', methods = ['POST'])
def friend():
    return render_template('friend.html')

@app.route('/emergency', methods = ['POST'])
def emergency():
    return render_template('emergency.html')

@app.route('/mypage', methods = ['POST'])
def mypage():
    return render_template('mypage.html')

@app.route('/schedule_page', methods = ['POST'])
def schedule_page():
    return render_template('schedule_page.html')

@app.route('/meet_successful', methods = ['POST'])
def meet_successful():
    return render_template('meet_successful.html')

@app.route('/meet_unsuceessful', methods = ['POST'])
def meet_unsucessful():
    return render_template('meet_unsuccessful.html')

@app.route('/chatting', methods = ['POST'])
def chatting():
    return render_template('chatting.html')

@app.route('/add_sch')
def add_sch():
    print('서비스를 추가합니다.')

    return '추가완료'

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)

