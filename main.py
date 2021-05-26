
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
from flask import jsonify


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'abiduduidudu'
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
#db = SQLAlchemy(app)
app.secret_key = 'my number one'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Orac135421'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return render_template('intro.html')#,posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/userLogin", methods=['GET', 'POST'])
def userLogin():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            # Redirect to home page
            return redirect(url_for('userHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('login.html', msg=msg)


@app.route("/managerLogin", methods=['GET', 'POST'])
def managerLogin():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM databasemanager WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('login.html', msg=msg)

@app.route("/userHome", methods=['GET', 'POST'])
def userHome():
    return render_template("userhome.html")

@app.route("/userInteractionofaDrug", methods=['GET', 'POST'])
def userInteractionofaDrug():
    msg =''
    if request.method == 'POST' and 'main_drug' in request.form:
        # Create variables for easy access
        main_drug = request.form['main_drug']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT interacting_drug FROM Drug_Interaction WHERE main_drug =%s', (main_drug))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'

    return render_template('userInteractionofaDrug.html', msg=msg)

@app.route('/userAction2', methods=['GET', 'POST']) 
def userAction2():
    msg =''
    if request.method == 'POST' and 'drug_id' in request.form:
        # Create variables for easy access
        drug_id = request.form['drug_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM DRUGBANK WHERE drug_id =%s', (drug_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('userAction2.html', msg=msg)

@app.route('/userAction3')
def userAction3():
	return render_template('userAction3.html')

@app.route('/userAction4')
def userAction4():
	return render_template('userAction4.html')
if __name__=='__main__':
    app.run(debug=True)
