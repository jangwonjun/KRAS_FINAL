from flask import Flask, request, redirect, render_template, url_for, session
from modules.flex import login_system
from env import FLASK_ENUM, SQL

app = Flask(__name__, static_url_path='/static')
app.secret_key = FLASK_ENUM.SECRET_KEY

@app.route('/login', methods=['GET','POST'])
def login():
    next = '로그인이 필요합니다.'
    if request.method == 'POST': 
        kras_login_system = login_system() 
        id = request.form.get('id') 
        password = request.form.get('password') 
        print(id, password)  


        auth_inform = kras_login_system.new_login(id, password)

        print("정보")
        print(auth_inform)
        if auth_inform :
            next = '로그인성공'
            session["username"] = auth_inform[0] #세션에 저장
            session["userid"] = auth_inform[0][1]
            print(next)
            return render_template('index.html', state = next, user = auth_inform[0][0])
        
        else:
            status_code = "password_incorrect"
            return render_template('login.html',status_code = status_code)
    
    return render_template('login.html') 

@app.route('/main')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)