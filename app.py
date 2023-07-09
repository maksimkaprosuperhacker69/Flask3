from flask import Flask,request,redirect,session
import json
from datetime import datetime
from pathlib import Path
app = Flask(__name__)
app.secret_key='wqwqwdq'

@app.route("/")
def index():
    page = ""
    f = open("index.html", "r")
    page += f.read()
    if session.get('new'):
        page+='<h3 class="new_user">You are registered!<h3>'
        session['new']=False
    return page


@app.route("/login")
def login():
    page=''
    page+=open('login.html','r').read()
    if session.get('try'):
        page+='<h3 class="uncorrect_pass">неправильный логин или пароль<h3>'
        session['try']=False
    return page


@app.route("/login", methods=["POST"])
def do_login():
    form=request.form
    global user_login
    user_login=form['login']
    with open('static/json/users.json','r') as data_users:
        data_users=json.load(data_users)
        if form['login'] in data_users and form['password']==data_users[form['login']]['password']:
            session['login']=form['login']
            return redirect('/home')
        else:
            session['try'] = True
            return redirect('/login')

@app.route("/singup")
def singup():
    page=open('singup.html','r').read()
    return page

@app.route("/singup",methods=["POST"])
def do_singup():
    form=request.form
    path = Path('static/json/users.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    data[form['new_login']]={'password':form['new_password']}
    path.write_text(json.dumps(data, indent=4), encoding='utf-8')
    session['new']=True
    return redirect('/')


@app.route('/home')
def home():
    list1=[]
    q=0
    page=open('home.html','r').read()
    f=open('shab_message_notadmin.html','r').read()
    if user_login=='admin':
        f=open('shab_message_adm.html','r').read()
    
    path = Path('static/json/messages.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    for i in reversed(data):
        q+=1
        shab=f
        shab=shab.replace('{text}', i["text"])
        shab=shab.replace('{date}', i["time"])
        shab=shab.replace('{name}', i["login"])
        try:
            shab=shab.replace('{key}', i["time"])
        except:
            pass
        page=page+shab
        if q==5:
            break
    page=page.replace('{name1}', user_login)


        






    return page

@app.route('/home',methods=["POST"])
def do_home():
    form=request.form
    current_datetime = datetime.now()
    path = Path('static/json/messages.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    data.append({'text':form["text_message"],'time':f"{current_datetime.year}.{current_datetime.month}.{current_datetime.day}__{current_datetime.hour}:0{current_datetime.minute}",'login':user_login})
    path.write_text(json.dumps(data, indent=4), encoding='utf-8')
    return redirect('/home')


@app.route('/delete',methods=["GET"])
def delete():
    if user_login!='admin':
        return redirect('/home')
    result=request.values['id']
    path = Path('static/json/messages.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    for index,i in enumerate(data):
        print(i)
        print(result)
        if result in i['time']:
            data.pop(index)
    path.write_text(json.dumps(data, indent=4), encoding='utf-8')
    return redirect('/home')







app.run(host = '0.0.0.0',port =80)
