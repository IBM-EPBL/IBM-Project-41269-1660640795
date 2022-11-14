
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb ;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=certificate.crt;UID=mxg10761;PWD=KVnpo9UEHot0k65L",'','')

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adminlogin.html')
def adminlogin():
    global userId
    msg=""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.excute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account["USERNAME"]
            msg = 'logged in successful!'

            return render_template('admindashboard.html',msg=msg);
        
        else: msg='Incorrect username / password!'
    return render_template('login.html',msg=msg)

    @app.route('/register',methods =['GET','POST'])
    def regiter():
        msg =''
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            sql ="SELECT  * FROM users where username =?"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
                msg = 'Invalid email address'
            elif not re.match(r'[A-Za-z0-9]+',username):
                msg = 'Name must contain only characters and numbers'
            else:
                insert_sql = "INSERT INTO users VALUES(?,?,?)"
                prep.stmt = ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,password)
                ibm_db.execute(prep_stmt)
                msg = 'You have successfully registered!'
        elif request.method == 'POST':
                msg ='Please fill out the form'
        return render_template('register.html',msg=msg)

@app.route('/admindashboard')
def dash():
    return render_template('admindashboard.html',methods=['GET','POST'])



if __name__ =='__main__':
    app.run(host='0.0.0.0')
