from flask import Flask, render_template, request, redirect, session
import pymysql
from hashlib import md5
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def create_connection():
    # Returns a connection to the specified database
    return pymysql.connect(  
        host = '127.0.0.1',
        user = 'ahmkhalaf',
        password = 'ARNAS',
        db = 'ahmkhalaf_app_database',
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )

@app.route('/')
def home_page():
    # Get all games from database, display in template
    connection = create_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users;"
        cursor.execute(sql)
        users = cursor.fetchall() # fetchall() - multiple records
        connection.close()
    return render_template("login.html", users = users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Create a record
    print("here!")
    # Check whether form has been submitted. Either process form data or render form, depending
    if request.method=="POST":
        connection = create_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO users(UserName, Password, FirstName, Surname) VALUES(%s,%s,%s, %s);"
            password = request.form["Password"]
            password = md5(password.encode()).hexdigest()
            print(password)
            vals = (request.form["UserName"], password, request.form["FirstName"], request.form["Surname"])
            cursor.execute(sql, vals)
            connection.commit() # The extra line needed for INSERT, UPDATE and DELETE
        connection.close()
        return redirect("/login") # Don't forget the redirect import!
    else:
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        connection = create_connection()
        with connection.cursor() as cursor:
            password = request.form["Password"]
            password = md5(password.encode()).hexdigest()
            sql = "SELECT UserName, Password FROM users WHERE UserName = %s AND Password = %s;"
            vals = (request.form ["UserName"], password)
            cursor.execute(sql, vals)
            user = cursor.fetchall()
        connection.close()

        if len(user) == 0:
            return render_template("login.html")

        session["loggedIn"] = True
        return redirect("/homepage") # Don't forget the redirect import!
    else:
        return render_template("login.html")
   
#@app.route('/admin')
#def admin():
#    if "loggedIn" in session:
#        return redirect("/homepage")
#    else:
#        return redirect("/")

#@app.route('/homepage', methods=['GET', 'POST'])
#def home_page1():
#    connection = create_connection()
#    if request.method == "POST":
#        with connection.cursor() as cursor:
#            if session["accessLevel" == 1]:
#                sql = "SELECT * FROM users WHERE name = %s, pegi = '-';"
#            else:
#                sql = "SELECT * FROM users WHERE name = %s;"
#            vals = (request.form['search'])
#            cursor.execute(sql, vals)
#            users = cursor.fetchall()
#            connection.close()
#            print(users)
#        return render_template("index.html", users = users)
#    else:
#        with connection.cursor() as cursor:
#            sql = "SELECT * FROM users;"
#            cursor.execute(sql)
#            users = cursor.fetchall()
#            connection.close()
#        return render_template("index.html", users = users)

@app.route("/homepage", methods=["GET", "POST"])
def home_page1():
    connection = create_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM shows;"
        cursor.execute(sql)
        user = cursor.fetchall()
        connection.close()
        return render_template("index.html", user = user)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    #delete a record
    #Get the idusers frm the url
    idusers = request.args['idusers']
    connection = create_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM users WHERE idusers=%s;"
        vals = (idusers)
        cursor.execute(sql, vals)
        connection.commit()
    connection.close()
    return redirect('/homepage')
        
@app.route('/create', methods=['GET','POST'])
def create():
   if request.method=="POST":
       connection = create_connection()
       with connection.cursor() as cursor:
           sql = "INSERT INTO users(UserName, Password, FirstName, Surname) VALUES(%s,%s,%s, %s);"
           vals = (request.form["name"], request.form["publisher"])
           cursor.execute(sql, vals)
           connection.commit()
       connection.close()
       return redirect("/")
   else:
       return render_template("create.html")

@app.route('/update', methods=['GET','POST'])
def updateform():
    idShows = request.args['idShows']
    connection = create_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM shows WHERE idShows=%s;"
        vals = (idShows)
        cursor.execute(sql, vals)
        selected_UserName = cursor.fetchone()
        connection.close()
    return render_template("update.html", selected_ShowName = selected_ShowName)


@app.route('/performupdate', methods=['GET','POST'])
def performupdate():
    connection = create_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE shows SET ShowName=%s, ShowDescription=%s WHERE idShows=%s;"
        vals = (request.form["ShowName"],
                request.form["ShowDescription"],
                request.form["idShows"],
                )
        cursor.execute(sql, vals)
        connection.commit()
    connection.close()
    return redirect("/homepage")


if __name__ == '__main__':
    import os
    app.secret_key = os.urandom(12)
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)