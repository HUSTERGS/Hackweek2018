from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hackweek2018'

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
    cursor.execute(
        "select * from users where useremail = %s and userpw = %s", (useremail, password))
    result = cursor.fetchall()
    if (result == []):
        return '用户不存在或密码错误'
        # flash('用户名不存在或密码错误')
        # return render_template('login.html')
    else:
        print(result[0][0])
        session['login_user'] = result[0][0]
        return redirect(url_for('homepage'))


@app.route('/home', methods=['GET'])  # response the homepage request
def homepage():
    return render_template('index.html')


@app.route('/ex', methods=['GET'])
def ex():
    flash('cdas')
    return 'cdsacdsacdsa'


@app.route('/logout')
def logout():
    session.pop('login_user', None)
    return redirect(url_for('homepage'))


@app.context_processor
def my_context_processor():
    login_user = session.get('login_user', '')
    return {'login_user': login_user}


if __name__ == '__main__':
    app.run(debug=True)
