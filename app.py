from flask import Flask, redirect, url_for, render_template, request, session
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    
db.create_all()
    

#using an array for testing purposes, ease of use :)
login = [ ['admin@gmail.com', 'admin', 'admin123'] ]


@app.route("/")
def home():
    users = Users.query.all()
    return render_template("index.html", users=users)


@app.route("/login", methods=['POST', 'GET'])
def login():
    
    #If the request is a post, it comes from login page, we handle the request here.
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        #Creating a query, using username as a key.
        query = Users.query.filter_by(username=username).first()
        
        # "if query" checks to see if there is a username in the database.
        if query:
            #if the username query equals the username we took from the form (same with password), user is logged in.
            if query.username == username and query.password == password:
                if query.username == 'admin':
                    admin = True
                    users = Users.query.all()
                    return render_template('index.html', username=username, admin = admin, users=users)
                
                return render_template('index.html', username=username)
        else:
            return render_template("login.html")
    #Finally, if the request is not a post OR if the login details are incorrect, we redirect to the login page.
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        

        if email and username and password:
            
            new_User = Users(email = email, username=username, password=password)
            db.session.add(new_User)
            db.session.commit()
            return render_template('index.html')
        else:
            return '/404'
    else: 
        return render_template("register.html")

@app.route('/aboutus')
def aboutUs():
    return render_template("about.html")

#error handling :)
@app.errorhandler(404)
def page_not_found(e):
    error = True
    return render_template('index.html', error=error)
    
