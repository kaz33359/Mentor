from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) #setting app variable with flask instancce

app.config['SECRET_KEY'] = '5973c53e6d26093ab3e5e1b1caa8d407'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager =LoginManager(app)

from mentor import routs
