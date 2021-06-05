
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

#to update affinity values of a reaction id
@app.route("/req3Affinity", methods=['GET', 'POST'])
def req3Affinity():
    if request.method == 'POST' and 'reaction_id' in request.form and 'affinity' in request.form :
        # Create variables for easy access
        reaction_id = request.form['reaction_id']
        affinity = request.form['affinity']
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT reaction_research.reaction_id FROM reaction_research WHERE reaction_id = {}'.format(reaction_id))
        if cursor.fetchone() is None:
            return "<h1>Given reaction not found</h1>"
        
        try:
            cursor.execute('UPDATE reaction_research SET affinity ={} WHERE reaction_id ={}'.format(affinity, reaction_id))
            con.commit()
            return ("<h1>Update Succesful</h1>")
        except Exception as err:
            return Response(str(err), status=403)


    return render_template('req3Affinity.html')

#to delete drugs. the tables should be designed in the on delete cascade fashion to succesfully work
@app.route("/req3Drug", methods=['GET', 'POST'])
def req3Drug():
    if request.method == 'POST' and 'drug_id' in request.form :
        # Create variables for easy access
        drug_id = request.form['drug_id']
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT drugbank.drug_id FROM drugbank WHERE drug_id = '{}'".format(drug_id))
        if cursor.fetchone() is None:
            return "<h1>Given drug is not found</h1>"
        try:
            cursor.execute("DELETE FROM drugbank WHERE drug_id ='{}'".format(drug_id))
            con.commit()
            return ("<h1>Delete Succesful</h1>")
        except Exception as err:
            return Response(str(err), status=403)       

    return render_template('req3Drug.html')  

#to delete drugs. the tables should be designed in the on delete cascade fashion to succesfully work
@app.route("/req4Prot", methods=['GET', 'POST'])
def deleteProtein():
    if request.method == 'POST' and 'uniprot_id' in request.form :
        # Create variables for easy access
        uniprot_id = request.form['uniprot_id']
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT uniprot.uniprot_id FROM uniprot WHERE uniprot_id = '{}'".format(uniprot_id))
        if cursor.fetchone() is None:
            return "<h1>Given protein is not found</h1>"
        try:
            cursor.execute("DELETE FROM uniprot WHERE uniprot_id ='{}'".format(uniprot_id))
            con.commit()
            return ("<h1>Delete Succesful</h1>")
        except Exception as err:
            return Response(str(err), status=403)       

    return render_template('req4Prot.html')  

#see users ?
@app.route("/managerSeeUsers", methods=['GET', 'POST'])
def seeUsers():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM users")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall()) 

#see drugs in drugbank ?
@app.route("/managerSeeDrugs", methods=['GET', 'POST'])
def seeDrugs():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM drugbank")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall())
#see proteins in uniprot ?
@app.route("/managerSeeProteins", methods=['GET', 'POST'])
def seeProtein():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM uniprot")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall()) 

#see side effects in sideeffect ?
@app.route("/managerSeeSiders", methods=['GET', 'POST'])
def seeSiders():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM sideeffect")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall()) 

#see Papers ?
@app.route("/managerSeePapers", methods=['GET', 'POST'])
def seePapers():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""SELECT p.doi, GROUP_CONCAT(u.name SEPARATOR '; ') as authors
                        from contribution_paper as p , users as u 
                        where u.username = p.username and u.institution = p.institution
                        group by p.doi""")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall())

#see Papers ?
@app.route("/managerSeeBindings", methods=['GET', 'POST'])
def seeBindings():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""select b.reaction_id, b.drug_id, d.drug_name, b.uniprot_id, p.target_name from bindingdb as b, drugbank as d, uniprot as p
where b.drug_id = d.drug_id and b.uniprot_id = p.uniprot_id""")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall()) 


#see Drugs and Interactions ?
@app.route("/userSeeDetailedDrug", methods=['GET', 'POST'])
def seeDetailedDrug():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""SELECT  d.drug_id, d.drug_name, d.smiles, d.description_, Z.target_names, Z.side_effect_names
                            FROM drugbank as d 
                            LEFT JOIN (SELECT *
                            FROM (select d.drug_id AS dr1,  GROUP_CONCAT(e.side_effect_name SEPARATOR ', ') as side_effect_names
                            from drugbank as d, SIDER as s, sideeffect as e
                            where d.drug_id = s.drug_id and s.umls_cui = e.umls_cui
                            GROUP BY d.drug_id) as X  LEFT JOIN (select  b.drug_id as dr2, GROUP_CONCAT(u.target_name SEPARATOR ', ') as target_names
                            from bindingdb as b, uniprot as u
                            where b.uniprot_id = u.uniprot_id
                            group by b.drug_id) as Y ON X.dr1 = Y.dr2
                            UNION
                            SELECT * 
                            FROM (select d.drug_id as dr1,  GROUP_CONCAT(e.side_effect_name SEPARATOR ', ') as side_effect_names
                            from drugbank as d, SIDER as s, sideeffect as e
                            where d.drug_id = s.drug_id and s.umls_cui = e.umls_cui
                            GROUP BY d.drug_id) as X  RIGHT JOIN (select  b.drug_id as dr2, GROUP_CONCAT(u.target_name SEPARATOR ', ') as target_names
                            from bindingdb as b, uniprot as u
                            where b.uniprot_id = u.uniprot_id
                            group by b.drug_id) as Y ON X.dr1 = Y.dr2) AS Z ON d.drug_id = Z.dr1 OR d.drug_id = Z.dr2""")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall()) 

@app.route("/userInteractionofaDrug", methods=['GET', 'POST'])
def userInteractionofaDrug():
    msg =''
    if request.method == 'POST' and 'main_drug' in request.form:
        # Create variables for easy access
        main_drug = request.form['main_drug']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT interacting_drug FROM Drug_Interaction WHERE main_drug ='{}'".format(main_drug))
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
        cursor.execute("SELECT SIDER.drug_id, SideEffect.side_effect_name FROM SideEffect INNER JOIN SIDER ON SIDER.umls_cui=SideEffect.umls_cui WHERE SIDER.drug_id='{}'".format(drug_id))
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
        cursor.execute("SELECT BindingDB.uniprot_id, Uniprot.target_name FROM BindingDB INNER JOIN Uniprot ON BindingDB.uniprot_id=Uniprot.uniprot_id WHERE BindingDB.drug_id='{}'".format(drug_id))
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
        cursor.execute("SELECT Drugbank.drug_id, Drugbank.drug_name FROM BindingDB INNER JOIN Drugbank ON BindingDB.drug_id=Drugbank.drug_id WHERE BindingDB.uniprot_id='{}'".format(uniprot_id))
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
        cursor.execute("SELECT Drugbank.drug_id, Drugbank.drug_name FROM SIDER INNER JOIN Drugbank ON Drugbank.drug_id = SIDER.drug_id WHERE SIDER.umls_cui ='{}'".format(umls_cui))
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
        cursor.execute("SELECT * FROM Drugbank WHERE description_ LIKE '{}'".format(keyword))
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
        cursor.execute("""select drug_id, count(*) as total from  
                        (select distinct SIDER.drug_id,SIDER.umls_cui,
                        uniprot_id from SIDER 
                        INNER JOIN BindingDB 
                        ON SIDER.drug_id=BindingDB.drug_id 
                        WHERE uniprot_id = '{}') as b 
                        group by drug_id 
                        having total in ( 
                        select min(total) from (select 
                        count(*) as total from 
                        (select distinct SIDER.drug_id,SIDER.umls_cui,
                        uniprot_id from SIDER 
                        INNER JOIN BindingDB 
                        ON SIDER.drug_id=BindingDB.drug_id 
                        WHERE uniprot_id = '{}') as b2 
                        group by drug_id)as b3)""".format(uniprot_id,uniprot_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('user17.html', msg=msg)   

#see Papers ?
@app.route("/userSeePapers", methods=['GET'])
def userSeePapers():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""SELECT p.doi, GROUP_CONCAT(u.name SEPARATOR '; ') as authors
                        from contribution_paper as p , users as u 
                        where u.username = p.username and u.institution = p.institution
                        group by p.doi""")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall())

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