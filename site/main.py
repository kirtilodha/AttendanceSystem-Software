import pymysql
pymysql.install_as_MySQLdb()
from flask_mail import Mail
from werkzeug.utils import secure_filename
#from werkzeug import secure_filename
from flask import Flask,render_template,request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import os
import math
with open('config.json','r') as c:
    params=json.load(c)['params']
app=Flask(__name__)
app.secret_key='super-secret-key'
db = SQLAlchemy(app)
local_server=True

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

class Id(db.Model):
    time = db.Column(db.Integer, primary_key=True)
    day= db.Column(db.String(80), nullable=False)
    semester= db.Column(db.String(20), nullable=False)
    subject= db.Column(db.String(12), nullable=False)
class Usnlist(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    attendance = db.Column(db.String(20), nullable=False)
@app.route("/",methods=['GET','POST'])
def home():
    if ('user' in session and session['user'] == params['admin_user']):
        id = Id.query.all()
        usnlist=Usnlist.query.all()
        return render_template('dashboard.html', params=params, id=id,usnlist=usnlist)
    if (request.method == 'POST'):
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            id= Id.query.all()
            return render_template('dashboard.html', params=params,id=id,usnlist=usnlist)

    return render_template('login.html', params=params)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():

    #usnlist = usnlist[(u - 1) * int(params["no_of_usn"]):(u - 1) * int(params["no_of_usn"]) + int(params["no_of_usn"])]
    if(request.method=="GET"):
        usnlist = Usnlist.query.filter_by().all()
        last = math.ceil(len(usnlist) / int(params['no_of_usn']))
        u = request.args.get('u', 3)
        print("usn", u)

        if (not str(u).isnumeric()):
            u = 1

        u= int(u)
        usnlist = usnlist[(u- 1) * int(params["no_of_usn"]):(u - 1) * int(params["no_of_usn"]) + int(params["no_of_usn"])]
        if (u== 1):
            u = "/dashboard"
            u= u + 1  #"/dashboard/?u=" + str(u+1)

        elif (u== last):
            u = u - 1
            u = "/dashboard"

        else:
            u = u - 1
            u= u + 1
        print(u,"u")
        #usnlist = usnlist[(u - 1) * int(params["no_of_usn"]):(u - 1) * int(params["no_of_usn"]) + int(params["no_of_usn"])]
        return render_template('dashboard.html', params=params, usnlist=usnlist,u=u)


    return render_template('dashboard.html')

@app.route("/present/<string:usn>")
def present(usn):
    usn= Usnlist.query.filter_by(usn=usn).first()
    usn.attendance="P"
    db.session.commit()
    return render_template("dashboard.html",usn=usn)

@app.route("/absent/<string:usn>")
def absent(usn):
    usn = Usnlist.query.filter_by(usn=usn).first()
    usn.attendance = "A"
    db.session.commit()
    return render_template("dashboard.html", usn=usn)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')






app.debug=True
app.run()
app.run(debug=True)
