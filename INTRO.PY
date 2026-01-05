from flask import Flask , render_template , request ,session ,redirect
import sqlite3 ,random
from datetime import timedelta
from flask_mail import Mail,Message

# print(__name__)
conn=sqlite3.connect('form.db',check_same_thread = False)
cur=conn.cursor()

#order page table
cur.execute (''' create table  if not exists od (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    phone BIGINT,
    bouquet TEXT,
    date VARCHAR(20),
    time VARCHAR(20),
    address TEXT,
    message TEXT)''')

#register page table

cur.execute (''' create table  if not exists reg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    email VARCHAR(50) ,
    phone BIGINT ,
    password VARCHAR(20))''')


app=Flask(__name__)
app.secret_key='laks'
app.permanent_session_lifetime=timedelta(minutes=10)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']='muthulakshmichitra73@gmail.com'
app.config['MAIL_PASSWORD']='teon ihuk dykr bhgj'
app.config['MAIL_USE_TLS']=True
a=Mail(app)

@app.route('/mail')
def mail():
    otp=random.randint(1000,5000)
    session['uotp']=otp
    
    b=Message(' your OTP here',sender='muthulakshmichitra73@gmail.com',recipients=['rahilak2801@gmail.com'])
    b.body=f"your otp {otp} valid upto 20 mins"
    
    try:
        a.send(b)
        return redirect('/otp')
    
    except Exception as e :
        return str(e)

@app.route('/otp',methods = ['GET','POST'])
def otp():
    if request.method == 'POST':
        userotp = request.form.get('o1')
        realotp= str(session.get('uotp'))
        
        if userotp == realotp:
            return redirect ('/login')
        
    return render_template('otp.html')
        
@app.route('/')
def home():
    if 'lemail' in session :
        #user = session['lemail']
        return render_template('home.html')
    return redirect ('/create')

#login page
@app.route('/login',methods = ['GET','POST'])
def login() :
    if request.method == 'POST':
        eemail = request.form.get ('lemail')
        login = request.form.get ('lpassword')
        cur.execute('select *from reg where email = ?', (eemail,)) 
        data = cur.fetchone()
        
        if data is None :
            return render_template ('login.html')
        pp = data[4]
        if login == pp :
            session['lemail']=eemail
            session['lpassword']=login
            return redirect('/')
        else:
            return 'invaild'
    return render_template('login.html')

@app.route("/create", methods=['GET',"POST"])
def create():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get('email')
        phone = request.form.get("phone")
        password = request.form.get("password")
        b=('insert into reg(name,email,phone,password) values(?,?,?,?)')
        cur.execute(b,(name,email,phone,password))
        conn.commit()
        return redirect ('/mail')
    return render_template('create.html')

@app.route('/logout')
def logout():
    session.pop('lemail')
    return redirect('/login')

#-----------------------------------------------------------------------------------------------------------------
    
@app.route("/orderconfirm", methods=['GET',"POST"])
def orderconfirm():
    if request.method == 'POST':
        name = request.form.get("name")
        phone = request.form.get("phone")
        bouquet = request.form.get("bouquet")
        date = request.form.get("date")
        time = request.form.get("time")
        address = request.form.get("address")
        message = request.form.get("message")
        
        a=('insert into od(name,phone,bouquet,date,time,address,message) values(?,?,?,?,?,?,?)')
        cur.execute(a,(name,phone,bouquet,date,time,address,message))
        conn.commit()
        return  render_template('orderconfirm.html',
        name=name,phone=phone,bouquet=bouquet,date=date,
        time=time,address=address,message=message)
    return render_template('order.html')

@app.route('/view')
def view():
    
    cur.execute('select *from od')
    data=cur.fetchall()
    print(data)
    return render_template('view.html',data=data)

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        name = request.form.get("name")
        phone = request.form.get("phone")
        bouquet = request.form.get("bouquet")
        date = request.form.get("date")
        time = request.form.get("time")
        address = request.form.get("address")
        message = request.form.get("message")
        cur.execute('update od set name=?,phone=?,bouquet=?,date=?,time=?,address=?,message=? where id =?',
                    (name,phone,bouquet,date,time,address,message,id))
        conn.commit()
        return  render_template('orderconfirm.html',
        name=name,phone=phone,bouquet=bouquet,date=date,
        time=time,address=address,message=message)
    cur.execute('select *from od where id=?',(id,))
    data=cur.fetchone()
    return render_template('update.html',data=data)

@ app.route('/delete/<int:id>')
def delete(id):
    cur.execute('delete from od where id =?',(id,))
    conn.commit()
    return 'data deleted'

#-----------------------------------------------------------------------------------------------------------------


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')
    
@app.route('/order')
def order():
    return render_template('order.html')


if __name__=='__main__':
    app.run(debug=True)
