import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

from flask_mail import Mail
from werkzeug.utils import secure_filename
# from werkzeug import secure_filename
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import os
import math
# from flask_mysqldb import MySQL
# import MySQLdb
# from flask_migrate import Migrate
import mysql.connector

with open('config.json', 'r') as c:
    params = json.load(c)['params']
app = Flask(__name__)
app.secret_key = 'super-secret-key'

local_server = True

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'MyDB'
# mysql = MySQL(app)
db = SQLAlchemy(app)
db2 = MySQLdb.connect("localhost", "root", "", "attendance")

cursor = db2.cursor()


# mydb = mysql.connector.connect(
#   host="localhost",
#   password="root",
#   user="root",
#   database="attendance"
# )

# mycursor = mydb.cursor()
# migrate = Migrate(app, db)
# cursor=db.cursor()
class Id(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(12), nullable=False)


class Id2(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(12), nullable=False)


class Usnlist(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    attendance = db.Column(db.String(20), nullable=False)


class Ii(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    attendance = db.Column(db.String(20), nullable=False)


class Iv(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    attendance = db.Column(db.String(20), nullable=False)

username=0
userpass=0
@app.route("/login", methods=['GET', 'POST'])
def home():
    if ('user' in session and session['user'] == params['admin_user1']):
        return redirect(url_for('dashboard'))
    if ('user' in session and session['user'] == params['admin_user2']):
        return redirect(url_for('dashboard'))
    if (request.method == 'POST'):
        global username
        global userpass
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        #print(username, userpass)
        if (username == params['admin_user1'] and userpass == params['admin_password1']):
            session['user'] = username

            return redirect(url_for('dashboard'))
        elif (username == params['admin_user2'] and userpass == params['admin_password2']):
            session['user'] = username
            return redirect(url_for('dashboard'))

        else:
            return render_template('login.html')

    return render_template('login.html', params=params)


print(username, userpass)
@app.route("/dashboard/")
def dashboard():
    x = datetime.datetime.now()
    current_time = x.strftime("%H")
    current_day = x.strftime("%A")
    #current_date = x.strftime("%x")
    current_date = x.strftime("%d%B%y")
    #print("inside dashboard")
    #print(username, userpass)
    # username="Riya"
    # userpass="hi"
    name="Riya"


    if (username == params['admin_user2'] and userpass == params['admin_password2']):
        id2 = Id2.query.filter_by(time="19", day="Tuesday").first()

        print(current_day)

        if (current_time == "19" and current_day == "Monday"):
            print(current_date)

            if (id2.semester == "IV" and id2.day == "Tuesday"):
                # q="IF EXISTS(SELECT * FROM information_schema.COLUMNS WHERE COLUMN_NAME = %s and TABLE_NAME = 'Iv' and TABLE_SCHEMA = 'attendance')" %(current_date)
                # q=cursor.execute(q)
                # if(not q):
                count = cursor.execute("SELECT * FROM information_schema.COLUMNS WHERE COLUMN_NAME = %s and TABLE_NAME = 'Iv' and TABLE_SCHEMA = 'attendance'",current_date)
                if count==0:
                    query = "ALTER IGNORE TABLE Iv ADD %s VARCHAR (40)" % (current_date)
                    cursor.execute(query)


                # if(query2):
                #     pass
                # else:
                #     query="ALTER TABLE Iv ADD %s VARCHAR (40)" %(current_date)
                #     cursor.execute(query)
                print(current_time)
                sem = Iv
                sem = sem.query.filter_by().all()
                last = math.ceil(len(sem) / int(params['no_of_usn']))
                u = request.args.get('u')

                if (not str(u).isnumeric()):
                    u = 1
                u = int(u)
                sem = sem[
                      (u - 1) * int(params["no_of_usn"]):(u - 1) * int(params["no_of_usn"]) + int(params["no_of_usn"])]
                if (u == 1):
                    prev = "#"
                    next = "/dashboard/?u=" + str(u + 1)

                elif (u == last):

                    prev = "/dashboard/?u=" + str(u - 1)

                    next = "#"

                else:
                    prev = "/dashboard/?u=" + str(u - 1)
                    next = "/dashboard/?u=" + str(u + 1)

                return render_template("dashboard.html", params=params, sem=sem, prev=prev, next=next)
            return render_template("dashboard.html", params=params)
        return render_template("dashboard.html", params=params)

    elif (username == params['admin_user1'] and userpass == params['admin_password1']):
        id = Id.query.filter_by(time=current_time, day=current_day).first()
        print(current_time, current_day)
        if (current_time == "14" and current_day == "Wednesday"):
            print(current_day)
            if (id.semester == "II"):
                print(id.day)
                sem = Ii
                print(id.semester)
                sem = sem.query.filter_by().all()
                last = math.ceil(len(sem) / int(params['no_of_usn']))

                v = request.args.get('v')

                if (not str(v).isnumeric()):
                    v = 1
                v = int(v)
                print(v)
                sem = sem[
                      (v - 1) * int(params["no_of_usn"]):(v - 1) * int(params["no_of_usn"]) + int(params["no_of_usn"])]

                if (v == 1):
                    prev = "#"
                    next = "/dashboard/?v=" + str(v + 1)

                elif (v == last):

                    prev = "/dashboard/?v=" + str(v - 1)

                    next = "#"

                else:
                    prev = "/dashboard/?v=" + str(v - 1)
                    next = "/dashboard/?v=" + str(v + 1)

                return render_template("dashboard.html", params=params, sem=sem, prev=prev, next=next)
            return render_template("dashboard.html", params=params)
        return render_template("dashboard.html", params=params)


@app.route("/present/<string:usn>")
def present(usn):
    usn = Ii.query.filter_by(usn=usn).first()
    usn.attendance = "P"
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route("/absent/<string:usn>")
def absent(usn):
    usn = Ii.query.filter_by(usn=usn).first()
    usn.attendance = "A"
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')


app.debug = True
app.run()
app.run(debug=True)
