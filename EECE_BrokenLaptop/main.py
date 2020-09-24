from datetime import datetime
from flask import Flask, render_template, request, redirect, redirect, url_for, session

import MySQLdb.cursors
import re
import os

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy 

# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other direcoty to keep it, 
# in that case the string will look different. 
#database = "sqlite:///brokenlaptops.db"
database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )


app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)


##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################

#@app.route('/init_db')
#def init_db():
#    db.drop_all()
#    db.create_all() 
#    return 'DB initialized'
   

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    return render_template('index.html', msg='')


    # Routes users to the home page
@app.route('/')
def index():
    brokenlaptops = BrokenLaptop.query.all()
    return render_template(
        "index.html",
        brokenlaptops=brokenlaptops,
        title='Home',
        year=datetime.now().year
    )
    

    # Displays laptops currently in the database
@app.route('/view')
def view():
    brokenlaptops = BrokenLaptop.query.all()
    return render_template(
        "view.html",
        brokenlaptops=brokenlaptops,
        title='View Laptops',
        year=datetime.now().year
    )


    # Creates entries in the database
@app.route('/create', methods=['GET','POST'])
def create():
   try:
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
        brokenlaptops = BrokenLaptop.query.all()
        return render_template("view.html",
                               brokenlaptops=brokenlaptops,
                               year=datetime.now().year
                               )
    
    return render_template(
        "create.html",
        title='Add Broken Laptop',
        year=datetime.now().year
    )
   except:
      return render_template(
        "create.html",
        error='Please complete form',
        title='Add Broken Laptop',
        year=datetime.now().year
    )
    
    # Deletes entries in the database
@app.route('/delete/<laptop_id>')
def delete(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    db.session.delete(brokenlaptop)
    db.session.commit()

    brokenlaptops = BrokenLaptop.query.all()
    return render_template(
                           "view.html",
                           brokenlaptops=brokenlaptops,
                           title='View Laptops',
                           year=datetime.now().year
                           )


    # Updates entries in the database
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = BrokenLaptop.query.get(request.form.get('id'))
 
        my_data.brand = request.form['brand']
        my_data.price = request.form['price']
 
        db.session.commit()
 
        brokenlaptops = BrokenLaptop.query.all()
        return render_template(
                               "view.html",
                               brokenlaptops=brokenlaptops,
                               title='View Laptops',
                               year=datetime.now().year
                               )


    #Renders the contact page
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Brandon Van Pelt'
    )


    #Renders the about page
@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='This application was developed for a class assignment in EECE 4081'
    )
    

# this class creates a table in the database named broken_laptop with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)

if __name__ == '__main__':
    app.run(debug=True)

# Added this code for the flask to work properly in visual studios
#if __name__ == '__main__':
#    import os
#    HOST = os.environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(os.environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)
    

