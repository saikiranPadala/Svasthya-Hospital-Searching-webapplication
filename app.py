from flask import Flask, g, redirect, render_template,request, session,url_for
import  copy
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="password",database="sai")
app = Flask(__name__, template_folder='templates')
app.secret_key = "somesecretkeythatishouldknow"


users=[]
@app.before_request
def before_request():
    g.user = None

    if'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def home():
    global a
    if request.method == "POST":
        disease=request.form.get('problem')
        if disease=='Cancer':
            a=1
        elif disease=='Covid-19':
            a=2
        elif disease=='Dengue':
            a=3
        elif disease=='Cardiology':
            a=4
        else:
            a=5
        scursor = mydb.cursor(buffered=True)
        q="SELECT h_name FROM hospitals,hd ""WHERE hd.d_Id = {} AND hd.h_Id = hospitals.Id_h".format(a)
        scursor.execute(q)
        data = scursor.fetchall()
        return render_template('hospital.html', data=data )


    return render_template('home.html')
@app.route('/hospitals', methods=['GET', 'POST'])
def hospital():
    if request.method == "POST":
        doc=request.form.get('h')
        if doc=='Tata memorial Hospital':
            x=1
        elif doc=='AIIMS':
            x=2
        elif doc=='RainBow':
            x=3
        elif doc=='KIMS':
            x=4
        else:
            x=5

        scursor = mydb.cursor(buffered=True)
        q = "SELECT d_name FROM doctors ""where s_Id={} and ho_Id={}".format(a,x)
        scursor.execute(q)
        data = scursor.fetchall()
        return render_template('doctor.html', data=data)
    return render_template('hospital.html')
@app.route('/doctors', methods=['GET', 'POST'])
def doctor():

    return render_template('doctor.html')

@app.route('/home', methods=['GET', 'POST'])
def index():

    return render_template('hhhhh.html')
@app.route('/signup', methods=['GET', 'POST'])
def sign():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        conform = request.form['conform']

        if password == conform:
             mycursor = mydb.cursor()
             mycursor.execute("INSERT INTO sup(fname ,lname , mobile, email, password) VALUES(%s, %s, %s, %s, %s)",(fname ,lname , mobile, email, password))
             mydb.commit()
             session['fname'] = fname
             session['lname'] = lname
             session['mobile'] = mobile
             session['email'] = email
             session['password'] = password

             return redirect(url_for('login'))
        else:
            return render_template('sup.html')

    return render_template('sup.html')
@app.route('/h1', methods=['GET', 'POST'])
def h1():

    return render_template('index4.html')
@app.route('/h2', methods=['GET', 'POST'])
def h2():

    return render_template('index5.html')
@app.route('/h3', methods=['GET', 'POST'])
def h3():

    return render_template('index6.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form['username']
        password = request.form['password']
        print(email,password)
        scursor = mydb.cursor(buffered=True)
        scursor.execute("SELECT  password, email,fname FROM sup WHERE email='" + email + "' AND password='" + password +"'")
        data = scursor.fetchone()
        non = copy.copy(data)
        if non is None :
            return redirect(url_for('login'))
        else:
            return render_template('index3.html')





    return render_template('login.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('p.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    mydb = mysql.connector.connect(host="localhost", user="root", password="password", database="munna")
    cur = mydb.cursor()
    cur.execute("select * from student_table")
    data = cur.fetchall()
    return render_template('table.html',data=data)

if __name__ == '__main__':
    app.run(debug = True)
