from bungalowpark import db

class Bungalow(db.Model):

    __tablename__ = 'bungalows'

    id = db.Column(db.Integer,primary_key = True)
    naam = db.Column(db.Text)
   
    # bungalow heeft een één-op-een relatie met type
    typeID = db.relationship('type',backref='bungalows',uselist=False)

    def __init__(self,naam,typeID):
        self.naam = naam
        self.typeID = typeID
    
    def __repr__(self):
        return f"De naam {self.name} en het type is  { self.typeID.aantalPersonen}"

class BungalowType(db.Model):

    __tablename__ = 'type'

    id = db.Column(db.Integer,primary_key= True)
    aantalPersonen = db.Column(db.Integer)
    weekprijs = db.Column(db.decimal)

    def __init__(self,aantalPersonen,weekprijs):
        self.aantalPersonen = aantalPersonen
        self.weekprijs = weekprijs

    def __repr__(self):
        return f"Dit type heeft plaats voor {self.aantalPersonen} personen en weekprijs is {self.weekprijs} "