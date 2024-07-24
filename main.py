from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage 
from datetime import datetime
import json

with open('config.json','r')as c:
    params=json.load(c)["params"]

local_server=True
app=Flask(__name__)
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key="super-secret-key"
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    phone=db.Column(db.String(50),nullable=False)
    message=db.Column(db.String(255),nullable=False)
    subject=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(12),nullable=False)

@app.route("/")
def home():
    return render_template('index.html',params=params)


@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=="POST"):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        subject=request.form.get('subject')
        entry=Contacts(name=name,email=email,phone=phone,message=message,subject=subject,date= datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)

@app.route("/work")
def work():
    return render_template('work.html',params=params)

app.run(debug=True)