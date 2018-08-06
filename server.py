from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
import mysql.connector
import datetime
from flask_avatar import Avatar
import json

app = Flask(__name__)
app.secret_key = 'hackweek2018'
Avatar(app)

con = mysql.connector.connect(
    user='root', password='MySQL#232', database='hackweek2018', port=3305, use_unicode=True)
cursor = con.cursor()


@app.route('/', methods=['GET'])  # response the login page request
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET'])  # response the register page request
def register():
    return render_template('register.html')


@app.route('/userregister', methods=['POST'])
def userregister():
    username = request.form.get('user')
    useremail = request.form.get('email')
    password = request.form.get('password1')
    cursor.execute("select * from users where username = %s", (username,))
    if (cursor.fetchall() == []):
        cursor.execute("insert into users (username, userpw, useremail) values (%s, %s, %s)",
                       (username, password, useremail))
        con.commit()
        print(username, useremail, password)
        return redirect(url_for('login'))
    else:
        return '该用户名已被使用'


@app.route('/userlogin', methods=['POST'])  # handle the login request
def userlogin():
    useremail = request.form.get('useremail')
    password = request.form.get('password')

    cursor.execute(
        "select * from users where useremail = %s and userpw = %s", (useremail, password))
    result = cursor.fetchall()
    if (result == []):
        flash('用户名不存在或密码错误')
        return render_template("login.html", **{'useremail': "" if (useremail == None) else useremail})

    else:
        print(result[0][0])
        session['login_user'] = result[0][0]
        return redirect(url_for('homepage'))


@app.route('/home', methods=['GET'])  # response the homepage request
def homepage():
    return render_template('index.html')


@app.route('/logout')  # logout and pop out user data
def logout():
    session.pop('login_user', None)
    return redirect(url_for('homepage'))


@app.route('/handledata', methods=['POST'])
def datahandler():
    data = request.get_data().decode()
    auth = session.get('login_user', '')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(session.get('login_user', ''))
    #print(data, auth, time)
    # print(data)
    cursor.execute(
        "insert into topics (topicname, topicauth, topictime, peoplenum) values (%s, %s, %s, %s)", (data, auth, time, 1))
    cursor.execute("create table " + time +
                   "('time' datetime not null, 'auth' varchar(30) not null, 'content' text not null)")
    con.commit()
    return redirect(url_for('homepage'))


@app.route('/discussdata/<sortway>', methods=['GET'])
def discussdata(sortway):
    if (sortway == 'newest'):
        cursor.execute(
            "select topicname, topicauth, cast(topictime as char) as topictime, peoplenum from topics order by topictime desc limit 0, 3;")
        result = cursor.fetchall()
        print(result)
        number = len(result)
        responseData = {}
        for num in range(number):
            responseData[num] = result[num]
        print(responseData)
        return jsonify(responseData)


@app.route('/talkdata/<sortway>', methods=['GET'])
def talkdata(sortway):
    if (sortway == 'numest'):
        cursor.execute(
            "select topicname, topicauth, cast(topictime as char) as topictime, peoplenum from topics order by peoplenum desc limit 0, 3;")
        result = cursor.fetchall()
        print(result)
        number = len(result)
        responseData = {}
        for num in range(number):
            responseData[num] = result[num]
        print(responseData)
        return jsonify(responseData)
    elif (sortway == 'newest'):
        cursor.execute(
            "select topicname, topicauth, cast(topictime as char) as topictime, peoplenum from topics order by topictime desc limit 0, 3;")
        result = cursor.fetchall()
        print(result)
        number = len(result)
        responseData = {}
        for num in range(number):
            responseData[num] = result[num]
        print(responseData)
        return jsonify(responseData)


@app.route('/ex')
def ex():
    print(session.get('login_user', ''))
    print(session.get('login_user', ''))
    print(session.get('login_user', ''))

    return session.get('login_user', '')


@app.route('/edite/<topic>')
def edite(topic):
    return render_template("editepage.html", **{'data': topic})


@app.context_processor  # handler
def my_context_processor():
    login_user = session.get('login_user', '')
    return {'login_user': login_user}


if __name__ == '__main__':
    app.run(debug=True)
