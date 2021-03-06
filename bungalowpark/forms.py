from bungalowpark.models import Bungalow, BungalowType, User, Boeking 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm',    message='Wachtwoorden moeten gelijk zijn!')])
    pass_confirm = PasswordField('Bevestig uw wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registeren!')
    
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een ander naam!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')

class BoekingForm(FlaskForm):
    # userID = StringField('userID', validators=[DataRequired()])
    bungalowID = HiddenField('bungalowID', validators=[DataRequired()])
    weeknummer =  HiddenField('weeknummer', validators=[DataRequired()])
    submit = SubmitField('Boek Nu!')

class BoekingUpdateForm(FlaskForm):
    bungalowID = HiddenField('bungalowID', validators=[DataRequired()])
    weeknummer =  HiddenField('weeknummer', validators=[DataRequired()])
    submit = SubmitField('Boek Nu!')