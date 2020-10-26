from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'neekendukuraa@mysql'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')

@app.route('/login',methods=['GET','POST'])

def login():
    msg=''
    if request.method=='POST' and 'mail_id' in request.form and 'passwd' in request.form:
        mail_id=request.form('mail_id')
        passwd = request.form('passwd')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from patient where mail_id = %s and passwd=% s',(mail_id,passwd,))

        if patient:
            session['loggedin'] = True
            session['mail_id'] = patient['mail_id']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('mail_id', None)
   return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form and 'P_name' in request.form and 'age' in request.form and 'blood_group' in request.form and 'sex' in request.form :
        mail_id = request.form['mail_id']
        passwd = request.form['passwd']
        P_name = request.form['P_name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        sex=request.form['sex']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE mail_id = % s', (mail_id, ))
        patient = cursor.fetchone()
        if patient:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO patient VALUES (NULL, % s, % s, % s, % s, % s, % s)', (mail_id, passwd, P_name, age, blood_group, sex,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (session['mail_id'], ))
        account = cursor.fetchone()
        return render_template("display.html", patient = patient)
    return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form and 'P_name' in request.form and 'age' in request.form and 'blood_group' in request.form and 'sex' in request.form :
            mail_id = request.form['mail_id']
            passwd = request.form['passwd']
            P_name = request.form['P_name']
            age = request.form['age']
            blood_group = request.form['blood_group']
            sex=request.form['sex']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (mail_id, ))
            patient = cursor.fetchone()
            if patient:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
                msg = 'Invalid email address !'
            else:
                cursor.execute('UPDATE accounts SET  mail_id =% s, passwd =% s, P_name =% s, age =% s, blood_group =% s, sex =%  WHERE mail_id =% s', (mail_id, passwd, P_name, age, blood_group, sex, (session['mail_id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg = msg)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
