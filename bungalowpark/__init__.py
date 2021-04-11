import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, login_required
# from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm



app = Flask(__name__)

app.config['SECRET_KEY'] = 'X11gc3N5hb78RGyKY4qk5qHZ8aqC4Ch7'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

from bungalowpark.models import BungalowType,Bungalow, User, Boeking 

# login = LoginManager()
# login.init_app(app)
# login.login_view = 'login'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/list')
def list_cur():
    # Maak een lijst van alle aanwezige cursisten in de database.
    bungalows = BungalowType.query.all()
    return render_template('test.html', bungalows=bungalows)

# @app.route('/loginpage', methods=("GET", "POST"))
# def loginpage():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')
