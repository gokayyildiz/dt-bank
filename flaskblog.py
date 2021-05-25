from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'abiduduidudu'
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
#db = SQLAlchemy(app)
app.secret_key = 'my number one'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc123'
app.config['MYSQL_DB'] = 'sample'

mysql = MySQL(app)


posts=[
    {
        'author':'Corey Schafer',
        'title':' Blog 1',
        'content': 'first content',
        'date':'May 24, 2021'

    },
    {
        'author':'Can Man',
        'title':' Blog 2',
        'content': 'second content',
        'date':'May 24, 2021'

    }
]

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
    msg =''
    return render_template('about.html')


if __name__=='__main__':
    app.run(debug=True)