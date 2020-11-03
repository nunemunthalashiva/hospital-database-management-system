from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)

app.secret_key = 'your secret key'
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
        mail_id=request.form['mail_id']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from patient where mail_id = % s and passwd= % s',(mail_id,passwd,))
        patient=cursor.fetchone()
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
        conn=mysql.connect
        cursor=conn.cursor()
        mail_id = request.form['mail_id']
        passwd = request.form['passwd']
        P_name = request.form['P_name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        sex=request.form['sex']
        cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (mail_id, ))
        patient = cursor.fetchone()
        if patient:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO patient VALUES (% s, % s, % s, % s, % s, % s)', (mail_id, passwd, P_name, age, blood_group, sex))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('index'))
    else:
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
        patient = cursor.fetchone()
        return render_template("display.html", patient = patient)
    return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form and 'P_name' in request.form and 'age' in request.form and 'blood_group' in request.form and 'sex' in request.form :
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id = request.form['mail_id']
            passwd = request.form['passwd']
            P_name = request.form['P_name']
            age = request.form['age']
            blood_group = request.form['blood_group']
            sex=request.form['sex']
            cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (mail_id, ))
            patient = cursor.fetchone()
            if not patient:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
                msg = 'Invalid email address !'
            else:
                cursor.execute('UPDATE patient SET  mail_id = % s, passwd = % s, P_name = % s, age = % s, blood_group = % s, sex = % s  WHERE mail_id = % s', (mail_id, passwd, P_name, age, blood_group, sex, (session['mail_id'], ), ))
                conn.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg = msg)
    return redirect(url_for('login'))
@app.route("/appointments")
def appointments():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM appointment WHERE mail_id = % s', (session['mail_id'], ))
        appointment=cursor.fetchall()
        return render_template("appointments.html", appointment = appointment)
    return redirect(url_for('login'))

@app.route('/makeappointment' , methods=['GET','POST'])
def makeappointment():
    msg=''
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'doctor_id' in request.form and 'date_appointment' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id = request.form['mail_id']
            doctor_id=request.form['doctor_id']
            date_appointment=request.form['date_appointment']
            cursor.execute('SELECT * FROM appointment WHERE mail_id = %s and date_appointment = %s',(mail_id,date_appointment))
            appointment=cursor.fetchone()
            if appointment:
                msg="you had already booked an appointment"
            else:
                cursor.execute('INSERT INTO appointment VALUES (%s,%s,%s)',(mail_id,date_appointment,doctor_id))
                conn.commit()
                msg='successfully booked your appointment!!'
                return redirect(url_for('index'))
        else:
            msg = 'appointment failed please rebook again!'
    return render_template('makeappointment.html', msg = msg)

@app.route('/receptionist_login',methods=['GET','POST'])
def receptionist_login():
    msg=''
    if request.method=='POST' and 'mail_id' in request.form and 'passwd' in request.form:
        mail_id=request.form['mail_id']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from receptionist where mail_id = % s and passwd= % s',(mail_id,passwd,))
        receptionist=cursor.fetchone()
        if receptionist:
            session['loggedin'] = True
            session['mail_id'] = receptionist['mail_id']
            msg = 'Logged in successfully !'
            return render_template('receptionist_index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('receptionist_login.html', msg = msg)

@app.route('/receptionist_logout')
def receptionist_logout():
    session.pop('loggedin', None)
    session.pop('mail_id', None)
    return redirect(url_for('receptionist_login'))

@app.route('/receptionist_register', methods =['GET','POST'])

def receptionist_register():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form and 'receptionist_name' in request.form :
        conn=mysql.connect
        cursor=conn.cursor()
        mail_id = request.form['mail_id']
        passwd = request.form['passwd']
        receptionist_name = request.form['receptionist_name']
        cursor.execute('SELECT * FROM receptionist WHERE mail_id = % s', (mail_id, ))
        receptionist = cursor.fetchone()
        if receptionist:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO receptionist VALUES (% s, % s, % s)', (mail_id, passwd, receptionist_name))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('receptionist_index'))
    else:
        msg = 'Please fill out the form !'
    return render_template('receptionist_register.html', msg = msg)

@app.route("/receptionist_index")
def receptionist_index():
    if 'loggedin' in session:
        return render_template("receptionist_index.html")
    return redirect(url_for('receptionist_login'))

@app.route("/receptionist_display")

def receptionist_display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM receptionist WHERE mail_id = % s', (session['mail_id'], ))
        receptionist = cursor.fetchone()
        return render_template("receptionist_display.html", receptionist = receptionist)
    return redirect(url_for('receptionist_login'))

@app.route("/receptionist_update", methods =['GET', 'POST'])
def receptionist_update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form and 'receptionist_name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id = request.form['mail_id']
            passwd = request.form['passwd']
            receptionist_name = request.form['receptionist_name']
            cursor.execute('SELECT * FROM receptionist WHERE mail_id = % s', (mail_id, ))
            receptionist = cursor.fetchone()
            if not receptionist:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
                msg = 'Invalid email address !'
            else:
                cursor.execute('UPDATE receptionist SET  mail_id = % s, passwd = % s, receptionist_name = % s WHERE mail_id = % s', (mail_id, passwd, receptionist_name,(session['mail_id'], ), ))
                conn.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("receptionist_update.html", msg = msg)
    return redirect(url_for('receptionist_login'))

@app.route('/doctor_login',methods=['GET','POST'])
def doctor_login():
    msg=''
    if request.method=='POST' and 'doctor_id' in request.form and 'passwd' in request.form:
        doctor_id=request.form['doctor_id']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from doctor where doctor_id = % s and passwd= % s',(doctor_id,passwd,))
        doctor=cursor.fetchone()
        if doctor:
            session['loggedin'] = True
            session['doctor_id'] = doctor['doctor_id']
            msg = 'Logged in successfully !'
            return render_template('doctor_index.html', msg = msg)
        else:
            msg = 'Incorrect doctor_id / password !'
    return render_template('doctor_login.html', msg = msg)

@app.route('/doctor_logout')
def doctor_logout():
    session.pop('loggedin', None)
    session.pop('doctor_id', None)
    return redirect(url_for('doctor_login'))

@app.route('/doctor_register', methods =['GET','POST'])

def doctor_register():
    msg = ''
    if request.method == 'POST' and 'doctor_id' in request.form and 'passwd' in request.form and 'availaible_date' in request.form and 'doctor_name' in request.form:
        conn=mysql.connect
        cursor=conn.cursor()
        doctor_id = request.form['doctor_id']
        passwd = request.form['passwd']
        doctor_name = request.form['doctor_name']
        availaible_date=request.form['availaible_date']
        cursor.execute('SELECT * FROM doctor WHERE doctor_id = % s', (doctor_id, ))
        doctor = cursor.fetchone()
        if doctor:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO doctor VALUES (% s, % s,% s, % s)', (doctor_id, passwd,doctor_name, availaible_date))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('doctor_index'))
    else:
        msg = 'Please fill out the form !'
    return render_template('doctor_register.html', msg = msg)

@app.route("/doctor_index")
def doctor_index():
    if 'loggedin' in session:
        return render_template("doctor_index.html")
    return redirect(url_for('doctor_login'))

@app.route("/doctor_display")

def doctor_display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE doctor_id = % s', (session['doctor_id'], ))
        doctor = cursor.fetchone()
        return render_template("doctor_display.html", doctor = doctor)
    return redirect(url_for('doctor_login'))

@app.route("/doctor_update", methods =['GET', 'POST'])
def doctor_update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'doctor_id' in request.form and 'passwd' in request.form and 'availaible_date' in request.form and 'doctor_name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            doctor_id = request.form['doctor_id']
            doctor_name=request.form['doctor_name']
            passwd = request.form['passwd']
            availaible_date = request.form['availaible_date']
            cursor.execute('SELECT * FROM doctor WHERE doctor_id = % s', (doctor_id, ))
            doctor = cursor.fetchone()
            if not doctor:
                msg = 'Account already exists !'
            else:
                cursor.execute('UPDATE doctor SET  doctor_id = % s, passwd = % s, doctor_name = % s,availaible_date= % s WHERE doctor_id = % s', (doctor_id, passwd, doctor_name,availaible_date,(session['mail_id'], ), ))
                conn.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("doctor_update.html", msg = msg)
    return redirect(url_for('doctor_login'))


if __name__ == "__main__":
    app.debug=True
    app.run(host ="localhost", port = int("5000"))
