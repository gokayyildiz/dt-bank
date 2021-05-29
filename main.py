
from flask import Flask, render_template, request, redirect, url_for, session,  Response
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
app.config['MYSQL_PASSWORD'] = 'abc123'
app.config['MYSQL_DB'] = 'sample'

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
            return redirect(url_for('managerHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('login.html', msg=msg)

@app.route("/userHome", methods=['GET', 'POST'])
def userHome():
    return render_template("userhome.html")

@app.route("/managerHome", methods=['GET', 'POST'])
def managerHome():
    return render_template("managerhome.html")

@app.route("/addUser", methods=['GET', 'POST'])
def addUser():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form and 'institution' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        institution = request.form['institution']
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("INSERT INTO Users(username, name, institution, password) VALUES (%s,%s,%s,%s)", (username, name, institution, password))
            con.commit()
            return ("<h1>Insertion Succesful</h1>")
        except Exception as err:
            return Response(str(err), status=403)

    return render_template('addUser.html')   

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


@app.route('/userdrugSideEffects', methods=['GET', 'POST']) 
def userdrugSideEffects():
    msg =''
    if request.method == 'POST' and 'drug_id' in request.form:
        # Create variables for easy access
        drug_id = request.form['drug_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SIDER.drug_id, SideEffect.side_effect_name FROM SideEffect INNER JOIN SIDER ON SIDER.umls_cui=SideEffect.umls_cui WHERE SIDER.drug_id=%s', (drug_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('userdrugSideEffects.html', msg=msg)    
    

@app.route('/userTargetsforSpecDrug', methods=['GET', 'POST'])
def userTargetsforSpecDrug():
    msg =''
    if request.method == 'POST' and 'drug_id' in request.form:
        # Create variables for easy access
        drug_id = request.form['drug_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT BindingDB.uniprot_id, Uniprot.target_name FROM BindingDB INNER JOIN Uniprot ON BindingDB.uniprot_id=Uniprot.uniprot_id WHERE BindingDB.drug_id=%s', (drug_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('userTargetsforSpecDrug.html', msg=msg)        

@app.route('/userInteractingDrugsforSpecProt', methods=['GET', 'POST'])
def userInteractingDrugsforSpecProt():
    msg =''
    if request.method == 'POST' and 'uniprot_id' in request.form:
        # Create variables for easy access
        uniprot_id = request.form['uniprot_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Drugbank.drug_id, Drugbank.drug_name FROM BindingDB INNER JOIN Drugbank ON BindingDB.drug_id=Drugbank.drug_id WHERE BindingDB.uniprot_id=%s   ', [uniprot_id])
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('userInteractingDrugsforSpecProt.html', msg=msg)        

@app.route('/user13', methods=['GET', 'POST'])
def user13():
    msg =''
    if request.method == 'POST':
        # Create variables for easy access
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT DISTINCT Uniprot.uniprot_id, BindingDB.drug_id FROM UniProt LEFT JOIN BindingDB ON Uniprot.uniprot_id = BindingDB.uniprot_id ORDER BY uniprot_id ASC, drug_id ASC')
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('user13.html', msg=msg)        

@app.route('/user14', methods=['GET', 'POST'])
def user14():
    msg =''
    if request.method == 'POST':
        # Create variables for easy access
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT  Drugbank.drug_id, BindingDB.uniprot_id FROM Drugbank LEFT JOIN BindingDB ON Drugbank.drug_id = BindingDB.drug_id ORDER BY drug_id ASC, uniprot_id ASC')
        return jsonify(data=cursor.fetchall())
    return render_template('user14.html', msg=msg)  

@app.route('/user15', methods=['GET', 'POST'])
def user15():
    msg =''
    if request.method == 'POST' and 'umls_cui' in request.form:
        # Create variables for easy access
        umls_cui = request.form['umls_cui']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Drugbank.drug_id, Drugbank.drug_name FROM SIDER INNER JOIN Drugbank ON Drugbank.drug_id = SIDER.drug_id WHERE SIDER.umls_cui = %s', [umls_cui])
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('user15.html', msg=msg)    

@app.route('/user16', methods=['GET', 'POST'])
def user16():
    msg =''
    if request.method == 'POST' and 'keyword' in request.form:
        # Create variables for easy access
        keyword = request.form['keyword']
        keyword = "%"+keyword+"%"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Drugbank WHERE description_ LIKE %s', [keyword])
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('user16.html', msg=msg)   

@app.route('/user17', methods=['GET', 'POST'])
def user17():
    msg =''
    if request.method == 'POST' and 'uniprot_id' in request.form:
        # Create variables for easy access
        uniprot_id = request.form['uniprot_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select drug_id, count(*) as total from ' 
                        '(select distinct SIDER.drug_id,SIDER.umls_cui,'
                        'uniprot_id from SIDER '
                        'INNER JOIN BindingDB '
                        'ON SIDER.drug_id=BindingDB.drug_id '
                        'WHERE uniprot_id = %s) as b '
                        'group by drug_id '
                        'having total in ( '
                        'select min(total) from (select '
                        'count(*) as total from '
                        '(select distinct SIDER.drug_id,SIDER.umls_cui,'
                        'uniprot_id from SIDER '
                        'INNER JOIN BindingDB '
                        'ON SIDER.drug_id=BindingDB.drug_id '
                        'WHERE uniprot_id = %s) as b2 '
                        'group by drug_id)as b3)', (uniprot_id,uniprot_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('user17.html', msg=msg)   


if __name__=='__main__':
    app.run(debug=True)


"""
13
SELECT DISTINCT Uniprot.uniprot_id, BindingDB.drug_id FROM UniProt 
LEFT JOIN BindingDB ON Uniprot.uniprot_id = BindingDB.uniprot_id
14
SELECT  Drugbank.drug_id, BindingDB.uniprot_id FROM Drugbank 
LEFT JOIN BindingDB ON Drugbank.drug_id = BindingDB.drug_id
15
SELECT Drugbank.drug_id, Drugbank.drug_name FROM SIDER 
INNER JOIN Drugbank 
ON Drugbank.drug_id = SIDER.drug_id
WHERE SIDER.umls_cui = %s
16
SELECT * FROM
Drugbank WHERE description_ LIKE '%{dummy string}%'
17
select drug_id, count(*) as total from 
(select distinct SIDER.drug_id,SIDER.umls_cui,
uniprot_id from SIDER
INNER JOIN BindingDB
ON SIDER.drug_id=BindingDB.drug_id
WHERE uniprot_id = 'uni1') as b
group by drug_id
having total in (
select min(total) from (select 
count(*) as total from 
(select distinct SIDER.drug_id,SIDER.umls_cui,
uniprot_id from SIDER
INNER JOIN BindingDB
ON SIDER.drug_id=BindingDB.drug_id
WHERE uniprot_id = 'uni1') as b2
group by drug_id)as b3)
"""