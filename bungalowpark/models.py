
from bungalowpark import db, app
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt(app)
class Bungalow(db.Model):

    __tablename__ = 'bungalows'

    id = db.Column(db.Integer(),primary_key = True)
    naam = db.Column(db.String(50), nullable=False, unique=True, index=True)
    # typeID =  db.Column(db.Integer(), nullable=False)
    typeID = db.Column(db.Integer,db.ForeignKey('type.id'))

    # bungalow heeft een één-op-een relatie met type
    # typeID = db.relationship('type',backref='bungalows',uselist=False)

    def __init__(self,naam,typeID):
        self.naam = naam
        self.typeID = typeID
    
    def __repr__(self):
        return f"De naam {self.naam} en het type is  { self.typeID.aantalPersonen}"

class BungalowType(db.Model):

    __tablename__ = 'type'

    id = db.Column(db.Integer(),primary_key= True)
    aantalPersonen = db.Column(db.Integer(), nullable=False )
    weekprijs = db.Column(db.Numeric(10,2), nullable=False)
    bungalow = db.relationship('Bungalow',backref='bungalowType',uselist=False)
    def __init__(self,aantalPersonen,weekprijs):
        self.aantalPersonen = aantalPersonen
        self.weekprijs = weekprijs

    def __repr__(self):
        return f"Dit type heeft plaats voor {self.aantalPersonen} personen en weekprijs is {self.weekprijs} "

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(),primary_key= True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self,username,password):
        self.username = username
        # self.password = generate_password_hash(password)
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # @login.user.loader
    # def load_user(user_id):
    #     return User.query.get(id)

    def __repr__(self):
        return f"De gebruikers naam is  {self.username}"

class Boeking(db.Model):

    __tablename__ = 'boekingen'

    id = db.Column(db.Integer(),primary_key= True)
    # userID = db.Column(db.Integer(25), nullable=False)
    # bungalowID = db.Column(db.Integer(25), nullable=False)
    weeknummer = db.Column(db.Integer(), nullable=False)
    # userID = db.relationship('User',backref='users', uselist=False)
    # bungalowID = db.relationship('Bungalow',backref='bungalows', uselist=False)
    def __init__(self,weeknummer,userID,bungalowID):
        self.weeknummer = weeknummer
        self.userID = userID
        self.bungalowID = bungalowID

  

    def __repr__(self):
        return f"de boeking is gedaan bij {self.userID.username} voor week  {self.weeknummer}. De bungalow is {self.bungalowID.naam}"

db.create_all()

# type1 = Bungalow('paarse bungalow',1)
# db.session.add_all([type1])

# # Vastleggen in de database
# db.session.commit()
# print(type1)