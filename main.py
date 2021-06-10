
from flask import Flask, render_template, request, redirect, url_for, session,  Response
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
from flask import jsonify
import hashlib

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

def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

@app.route("/")
def hello_world():
    return render_template('intro.html')#,posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/userLogin", methods=['GET', 'POST'])
def userLogin():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'institution' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password = hash_string(password)
        institution = request.form['institution']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s AND institution = %s', (username, password,institution))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['institution'] = account['institution']
            session['password'] = account['password']
            # Redirect to home page
            return redirect(url_for('userHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('userlogin.html', msg=msg)


@app.route("/managerLogin", methods=['GET', 'POST'])
def managerLogin():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password = hash_string(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM databasemanager WHERE username = %s AND password = %s', (username, password))
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


    return render_template('managerlogin.html', msg=msg)

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
        password = hash_string(password)
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
        
        cursor.execute('SELECT reaction_research.reaction_id FROM reaction_research WHERE reaction_id = "{}"'.format(reaction_id))
        if cursor.fetchone() is None:
            return "<h1>Given reaction not found</h1>"
        
        try:
            cursor.execute('UPDATE reaction_research SET affinity ={} WHERE reaction_id ="{}"'.format(affinity, reaction_id))
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

@app.route("/req5insertUser", methods=['GET', 'POST'])
def req5insertUser():
    if request.method == 'POST' and 'reaction_id' in request.form and 'username' in request.form and 'name' in request.form and 'password' in request.form  :
        # Create variables for easy access
        reaction_id = request.form['reaction_id']
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        password = hash_string(password)
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("""SELECT U.institution, username, password, name, doi from 
                            (SELECT DISTINCT @institution := C.institution, C.doi FROM Contribution_Paper C, Reaction_Research R WHERE
                            C.doi = R.doi and R.reaction_id = '{}') as t1, Users U
                            WHERE U.institution = @institution and
                            username = '{}' and password='{}' and   
                            name = '{}' """.format(reaction_id,username,password,name))
        decide =cursor.fetchone()
        
        if decide is not None:
            institution=decide['institution']
            doi = decide['doi']
            cursor.execute("""INSERT INTO Contribution_Paper 
                            Values ('{}','{}','{}') """.format(username,institution,doi))
            con.commit()                
            return ("Insertion is successful, no need to create a new user")

        else: #seeam seam burası boşsa şimdik user da yarataceuz
            cursor.execute("""select distinct C.doi, R.reaction_id, C.institution from 
            Contribution_Paper C, Reaction_Research R where C.doi=R.doi and R.reaction_id = '{}'; """.format(reaction_id))
            case2=cursor.fetchone()
            doi=case2['doi']
            institution=case2['institution']
            print(case2)
            cursor.execute("""insert into users values ('{}','{}','{}','{}') """.format(username,name,institution,password))
            cursor.execute("""insert into contribution_paper values ('{}','{}','{}')""".format(username,institution,doi))
            con.commit()
            return ("<h1>new user created, and inserted to the corresponding doi wrt the reaction_id<h1/>")
    return render_template('req5insertUser.html')  

#acaba burda passwordler falan neden veriliyor? 

@app.route("/req5deleteUser", methods=['GET', 'POST'])
def req5deleteUser():
    if request.method == 'POST' and 'reaction_id' in request.form and 'username' in request.form and 'name' in request.form and 'password' in request.form  :
        # Create variables for easy access
        reaction_id = request.form['reaction_id']
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        password = hash_string(password)
        con = mysql.connection
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""select distinct C.doi, R.reaction_id, C.institution from 
        Contribution_Paper C, Reaction_Research R where C.doi=R.doi and R.reaction_id = '{}'; """.format(reaction_id))
        case2=cursor.fetchone()
        institution=case2['institution']
        doi = case2['doi']
        cursor.execute("""select * from users where username = '{}' and name = '{}' and 
                        institution = '{}' 
                        and password = '{}' """.format(username,name,institution,password))
        if cursor.fetchone() is None:
            return ("There is no such user and paper to delete!")
        else:    
            cursor.execute("""delete from Contribution_Paper where 
            username = '{}' and institution = '{}' and doi = '{}'""".format(username,institution,doi))
            con.commit()
            return ("<h1>deletion successful<h1>")      

    return render_template('req5deleteUser.html')  



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
                            GROUP BY d.drug_id) as X  LEFT JOIN (select  b.drug_id as dr2, GROUP_CONCAT(DISTINCT u.target_name SEPARATOR ', ') as target_names
                            from bindingdb as b, uniprot as u
                            where b.uniprot_id = u.uniprot_id
                            group by b.drug_id) as Y ON X.dr1 = Y.dr2
                            UNION
                            SELECT * 
                            FROM (select d.drug_id as dr1,  GROUP_CONCAT(e.side_effect_name SEPARATOR ', ') as side_effect_names
                            from drugbank as d, SIDER as s, sideeffect as e
                            where d.drug_id = s.drug_id and s.umls_cui = e.umls_cui
                            GROUP BY d.drug_id) as X  RIGHT JOIN (select  b.drug_id as dr2, GROUP_CONCAT(DISTINCT u.target_name SEPARATOR ', ') as target_names
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
        cursor.execute("""select interacting_drug, drug_name from Drug_Interaction I, drugbank D where main_drug='{}' 
and D.drug_id=I.interacting_drug""".format(main_drug))
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
        cursor.execute("SELECT SIDER.umls_cui, SideEffect.side_effect_name FROM SideEffect INNER JOIN SIDER ON SIDER.umls_cui=SideEffect.umls_cui WHERE SIDER.drug_id='{}'".format(drug_id))
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
        cursor.execute("SELECT DISTINCT BindingDB.uniprot_id, Uniprot.target_name FROM BindingDB INNER JOIN Uniprot ON BindingDB.uniprot_id=Uniprot.uniprot_id WHERE BindingDB.drug_id='{}'".format(drug_id))
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
        cursor.execute("SELECT DISTINCT Drugbank.drug_id, Drugbank.drug_name FROM BindingDB INNER JOIN Drugbank ON BindingDB.drug_id=Drugbank.drug_id WHERE BindingDB.uniprot_id='{}'".format(uniprot_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'There is no such drug'
    return render_template('userInteractingDrugsforSpecProt.html', msg=msg)        

@app.route('/user13', methods=['GET', 'POST'])
def user13():
    msg =''
        # Create variables for easy access
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT DISTINCT Uniprot.uniprot_id, GROUP_CONCAT(DISTINCT BindingDB.drug_id SEPARATOR ', ') as drugs 
FROM UniProt LEFT JOIN BindingDB ON Uniprot.uniprot_id = BindingDB.uniprot_id 
GROUP BY  Uniprot.uniprot_id""")
    return jsonify(data=cursor.fetchall())
      

@app.route('/user14', methods=['GET', 'POST'])
def user14():
        # Create variables for easy access
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT  Drugbank.drug_id, GROUP_CONCAT(DISTINCT BindingDB.uniprot_id SEPARATOR ', ') as proteins 
FROM Drugbank LEFT JOIN BindingDB ON Drugbank.drug_id = BindingDB.drug_id 
GROUP BY  Drugbank.drug_id """)
    return jsonify(data=cursor.fetchall())


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
        cursor.execute("SELECT drug_id, drug_name, description_ FROM Drugbank WHERE description_ LIKE '{}'".format(keyword))
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
        cursor.execute("""select distinct t1.drug_id, drug_name, totals, uniprot_id from
(select D.drug_id, drug_name, count(*) as totals from drugbank D, SIDER S where d.drug_id=s.drug_id 
group by D.drug_id) as t1, bindingdb b where t1.drug_id=b.drug_id and b.uniprot_id='{}'
having totals in ( 
select min(totals) from (select distinct t1.drug_id, drug_name, totals, uniprot_id from
(select D.drug_id, drug_name, count(*) as totals from drugbank D, SIDER S where d.drug_id=s.drug_id 
group by D.drug_id) as t1, bindingdb b where t1.drug_id=b.drug_id and b.uniprot_id='{}') as t3)""".format(uniprot_id,uniprot_id))
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

@app.route("/userSeeRankings", methods=['GET'])
def userSeeRankings():
    con = mysql.connection
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""select * from institutions order by points desc""")
    except Exception as err:
        return Response(str(err), status=403)  
 
    return jsonify(data=cursor.fetchall())



@app.route('/userSeeFilteredTargets', methods=['GET', 'POST'])
def userSeeFilteredTargets():
    msg =''
    if request.method == 'POST' and 'measure_type' in request.form and 'min_affinity' in request.form and 'max_affinity' in request.form and 'drug_id' in request.form:
        # Create variables for easy access
        measure_type = request.form['measure_type']
        min_affinity= request.form['min_affinity']
        max_affinity= request.form['max_affinity']
        drug_id = request.form['drug_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""call getFilteredTargets('{}',{},{},'{}')""".format(measure_type, min_affinity,max_affinity,drug_id))
        return jsonify(data=cursor.fetchall())
    else:
        msg = 'Parameters are not suitably provided!'
    return render_template('userSeeFilteredTargets.html', msg=msg)   

if __name__=='__main__':
    app.run(debug=True)

