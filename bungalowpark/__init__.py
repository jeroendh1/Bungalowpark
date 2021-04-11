import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, login_required
# from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime, date


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
from bungalowpark.forms import LoginForm, RegistrationForm, BoekingForm

@app.route('/')
def index():
    bungalows = Bungalow.query.all()
    return render_template('home.html', bungalows=bungalows)

# @app.route('/list')
# def list_cur():
#     # Maak een lijst van alle aanwezige cursisten in de database.
#     bungalows = Bungalow.query.all()
#     return render_template('test.html', bungalows=bungalows)

@app.route('/bungalow/<bungalow>', methods=['GET', 'POST'])
def bungalow(bungalow):
    form = BoekingForm()
    # print(bungalow)
    bungalow = Bungalow.query.filter_by(naam=bungalow)
    # print(bungalow)
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        # Maak boeking met de gegevens van de gebruiker
        boeking = Boeking(userID=current_user.id,
                    bungalowID=form.bungalowID.data,
                    weeknummer=form.weeknummer.data)

        db.session.add(boeking)
        db.session.commit()
        flash('Het boeken van de bungalow is gelukt', 'success')
        return redirect(url_for('index'))
    return render_template('bungalow.html', valve=bungalow, bungalow=bungalow, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Je bent nu uitgelogd!', 'success')
    return redirect(url_for('index'))

@app.route('/boekingen')
@login_required
def boekingen():
    today = datetime.now()
    weeknummer = datetime.date(today).isocalendar()[1]
    # print(a)
    # ndate=date(c)
    # ndate = datetime.strptime(ndate, '%m/%d/%Y').strftime('%Y,%m,%d')
    # print('new format:',ndate)
    # d=ndate.split(',')
    # wkno = date(int(d[0]),int(d[1]),int(d[2])).isocalendar()[1]
    # print(wkno)
    # bungalow = Bungalow.query.filter_by(Boeking_id=1)
    nieuweBoekingen = Boeking.query.filter(Boeking.userID == current_user.id, Boeking.weeknummer > weeknummer)
    oudeBoekingen = Boeking.query.filter(Boeking.userID == current_user.id, Boeking.weeknummer <= weeknummer)
    return render_template('boekingen.html', nieuweBoekingen=nieuweBoekingen, oudeBoekingen=oudeBoekingen)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(u'Succesvol ingelogd.', 'success')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('index')
                return redirect(next)
        else:
            flash(u'U email of wachtwoord is niet correct.', 'warning')     
    # else: 
    #     flash(u'U email of wachtwoord is niet correct.', 'warning')              
    return render_template('login.html', form=form) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data != user.email and form.user.data != user.username: 
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash(u'Dank voor de registratie. Er kan nu ingelogd worden! ', 'success')
            return redirect(url_for('login'))
        elif form.email.data == user.email:
            flash(u'Dit e-mailadres staat al geregistreerd!', 'danger')
        else:
            flash(u'Deze gebruikersnaam is al vergeven, probeer een ander naam!', 'danger')

           
    return render_template('register.html', form=form)
