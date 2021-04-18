from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/index",methods=['GET','POST'])
def index():
    return render_template("index.html")

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
        return render_template('home.html')
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('mail_id', None)
   return redirect(url_for('home'))


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
            return redirect(url_for('login'))
    else:
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



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
        if request.method=='POST' and  'doctor_id' in request.form and 'date_appointment' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            doctor_id=request.form['doctor_id']
            date_appointment=request.form['date_appointment']
            cursor.execute('SELECT * FROM appointment WHERE mail_id = %s and date_appointment = %s',(session['mail_id'],date_appointment))
            appointment=cursor.fetchone()
            if appointment:
                msg="you had already booked an appointment"
            else:
                cursor.execute('INSERT INTO appointment VALUES (%s,%s,%s)',(session['mail_id'],date_appointment,doctor_id))
                conn.commit()
                msg='successfully booked your appointment!!'
                return redirect(url_for('index'))
        else:
            msg = 'appointment failed please rebook again!'
        return render_template('makeappointment.html', msg = msg)
    return redirect(url_for('login'))

@app.route('/donation',methods=['GET','POST'])
def donation():
    msg=''
    if 'loggedin' in session:
        if request.method=='POST' and  'donation_id' in request.form and 'donation_date' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            donation_id=request.form['donation_id']
            if(donation_id=='blood'):
                donation_id='500000'
            elif(donation_id=='plasma'):
                donation_id='500001'
            else:
                donation_id='500002'

            donation_date=request.form['donation_date']
            cursor.execute('SELECT * from donate where mail_id= % s and donation_id= % s and donation_date = % s',(session['mail_id'],donation_id,donation_date))
            donation=cursor.fetchone()
            if donation:
                msg='Hey you already signedup for donation'
            else:
                cursor.execute('INSERT into donate values(%s,%s,%s)',(session['mail_id'],donation_id,donation_date))
                conn.commit()
                msg='Thanks for your generosity'
                return redirect(url_for('index'))
        else:
            msg="Sorry please check your details before submitting"
        return render_template('donation.html',msg=msg)
    return redirect(url_for('login'))


@app.route('/receptionist_logout')
def receptionist_logout():
    session.pop('loggedin', None)
    session.pop('mail_id', None)
    return redirect(url_for('home'))

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

@app.route("/update_tests" , methods=["GET","POST"])
def update_tests():
    msg=" "
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'test_id' in request.form and 'test_date' in request.form and 'test_analysis' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            test_id=request.form['test_id']
            test_analysis=request.form['test_analysis']
            test_date=request.form['test_date']
            cursor.execute('INSERT INTO test_descrp values(%s,%s,%s,%s)',(mail_id,test_id,test_date,test_analysis))
            conn.commit()
            msg="Successfully updated"
            return render_template('receptionist_index.html',msg=msg)
        else:
            msg='please fill out the form'
    return render_template('update_tests.html', msg = msg)

@app.route("/takes",methods=["GET","POST"])
def takes():
    msg=''
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'medicine_id' in request.form and 'quantity' in request.form and 'takes_date' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            medicine_id=request.form['medicine_id']
            quantity=request.form['quantity']
            takes_date=request.form['takes_date']
            cursor.execute('INSERT into takes values(%s,%s,%s,%s)',(mail_id,medicine_id,quantity,takes_date))
            conn.commit()
            msg="successfully booked medicines"
            return render_template('receptionist_index.html',msg=msg)
        else:
            msg='please fill out the form'
    return render_template('takes.html', msg = msg)

@app.route("/update_record",methods=['GET','POST'])
def update_record():
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'record_id' in request.form and 'record_analysis' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            record_id=request.form['record_id']
            record_analysis=request.form['record_analysis']
            cursor.execute('INSERT into record values(%s,%s,%s)',(mail_id,record_id,record_analysis))
            conn.commit()
            msg="successfully booked medicines"
            return render_template('receptionist_index.html',msg=msg)
        else:
            msg='please fill out the form'
    return render_template('update_record.html', msg = msg)

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


@app.route('/nurse_info',methods=['GET','POST'])
def nurse_info():
    msg=''
    if 'loggedin' in session:
        if request.method=='POST' and 'nurse_id' in request.form and 'nurse_name' in request.form and 'phone_number' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            nurse_id=request.form['nurse_id']
            nurse_name=request.form['nurse_name']
            phone_number=request.form['phone_number']
            cursor.execute('SELECT * from nurse where nurse_id = % s',(nurse_id,))
            nurse=cursor.fetchone()
            if nurse:
                msg="Nurse account already exists"
            else:
                cursor.execute('INSERT into nurse values(%s,%s,%s)',(nurse_id,nurse_name,phone_number))
                conn.commit()
                msg="successfully nurse has registered"
                return render_template('receptionist_index.html',msg=msg)
    else:
        msg = 'Please fill out the form !'
    return render_template('nurse_info.html', msg = msg)

@app.route('/allocate_rooms',methods=['GET','POST'])
def allocate_rooms():
    msg=''
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'room_no' in request.form and 'block_no' in request.form  and'date_in' in request.form and 'date_out' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            room_no=request.form['room_no']
            block_no=request.form['block_no']
            date_in=request.form['date_in']
            date_out=request.form['date_out']
            cursor.execute('SELECT * from bookings where mail_id= % s and date_in = %s',(mail_id,date_in,))
            bookings = cursor.fetchone()
            if bookings:
                msg = 'You already booked your appointment !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
                msg = 'Invalid email address !'
            else:
                cursor.execute('INSERT INTO bookings(mail_id, room_no, block_no,date_in,date_out) VALUES (% s, % s, % s,% s,% s)', (mail_id, room_no, block_no,date_in,date_out))
                conn.commit()
                msg = 'You have successfully booked room for the patient !'
                return redirect(url_for('receptionist_index'))
        else:
            msg = 'Please fill out the form !'
            return render_template('allocate_rooms.html', msg = msg)



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
    return redirect(url_for('home'))

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


@app.route("/nurse_alloc",methods=['GET','POST'])
def nurse_alloc():
    if 'loggedin' in session:
        if request.method=='POST' and 'mail_id' in request.form and 'nurse_id' in request.form and 'date_in' in request.form and 'date_out' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            nurse_id=request.form['nurse_id']
            date_in=request.form['date_in']
            date_out=request.form['date_out']
            cursor.execute('INSERT into nursealloc VALUES(%s,%s,%s,%s,%s)',(session['doctor_id'],nurse_id,mail_id,date_in,date_out))
            conn.commit()
            msg="successfully allocated nurse"
            return render_template('doctor_index.html',msg=msg)
        else:
            msg='please fill out the form'
            return render_template('nurse_alloc.html', msg = msg)
    return render_template('doctor_login.html')
@app.route("/my_records",methods=['GET','POST'])
def my_records():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM record WHERE mail_id = % s', (session['mail_id'], ))
        record = cursor.fetchall()
        return render_template("my_records.html", record = record)
    return redirect(url_for('login'))

temp1=0

@app.route("/patient_record",methods=['GET','POST'])

def patient_record():
    if 'loggedin' in session:
        conn=mysql.connect
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM record WHERE mail_id = % s', (temp1, ))
        record=cursor.fetchall()
        return render_template("patient_record.html", record=record)
    return redirect(url_for('home'))

@app.route("/pre_patient_record",methods=['GET','POST'])

def pre_patient_record():
    msg=" "
    if 'loggedin' in session:
        if request.method=="POST" and 'mail_id' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=request.form['mail_id']
            temp1=mail_id
            return redirect(url_for('patient_record'))
        else:
            return render_template("pre_patient_record.html",msg=msg)
    return render_template('doctor_index.html')
temp2=0

@app.route("/rec_appointment",methods=['GET','POST'])
def rec_appointment():
    if 'loggedin' in session:
        conn=mysql.connect
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM appointment WHERE doctor_id = % s', (temp2,))
        appoint=cursor.fetchall()
        return render_template("rec_appointment.html", appoint=appoint)
    return redirect(url_for('home'))

@app.route("/pre_rec_appointment",methods=['GET','POST'])
def pre_rec_appointment():
    msg=" "
    if 'loggedin' in session:
        if request.method=="POST" and 'doctor_id' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            doctor_id=request.form['doctor_id']
            temp2=doctor_id
            return redirect(url_for('rec_appointment'))
        else:
            return render_template("pre_rec_appointment.html",msg=msg)
    return render_template('receptionist_index.html')

@app.route("/doctors_data",methods=['GET','POST'])
def doctors_data():
    return render_template('doctors_data.html')

if __name__ == "__main__":
    app.debug=True
    app.run(host ="localhost", port = int("5000"))
