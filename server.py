from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

con = mysql.connector.connect(
    user='root', password='MySQL#232', database='hackweek2018', port=3305, use_unicode=True)
cursor = con.cursor()


@app.route('/', methods=['GET'])  # response the login page request
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET'])  # response the register page request
def register():
    return render_template('register.html')


@app.route('/userlogin', methods=['POST', 'GET'])  # handle the login request
def userlogin():
    useremail = request.form.get('useremail')
    password = request.form.get('password')
    print(useremail, password)
    cursor.execute(
        "select * from users where useremail = %s and userpw = %s", (useremail, password))
    if (cursor.fetchall() == []):
        return '用户不存在或密码错误'
    else:
        return '登录成功'


@app.route('/home', methods=['GET'])  # response the homepage request
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
