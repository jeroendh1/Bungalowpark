import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, login_required
# from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user



app = Flask(__name__)

app.config['SECRET_KEY'] = 'X11gc3N5hb78RGyKY4qk5qHZ8aqC4Ch7'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)
Migrate(app, db)

from bungalowpark.models import BungalowType ,Bungalow, User, Boeking 
from bungalowpark.forms import LoginForm, RegistrationForm
# login = LoginManager()
# login.init_app(app)
# login.login_view = 'login'

@app.route('/')
def index():
    bungalows = Bungalow.query.all()
    return render_template('home.html', bungalows=bungalows)

@app.route('/list')
def list_cur():
    # Maak een lijst van alle aanwezige cursisten in de database.
    bungalows = Bungalow.query.all()
    return render_template('test.html', bungalows=bungalows)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('index'))

@app.route('/boekingen')
@login_required
def boekingen():
    return render_template('boekingen.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Succesvol ingelogd.')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('boekingen')
                return redirect(next)
                
    return render_template('login.html', form=form) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# @app.route('/loginpage', methods=("GET", "POST"))
# def loginpage():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')
