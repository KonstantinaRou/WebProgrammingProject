from app import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(512))
    admin = db.Column(db.Boolean,default=False)
    token = db.Column(db.String(512))

    def __init__(self, email, password):
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.email

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
	name = db.Column(db.String(50))
	surname = db.Column(db.String(50))
	birthdate =  db.Column(db.DateTime)
	website =  db.Column(db.String(50))
	address =  db.Column(db.String(50))
	telephone =  db.Column(db.String(50))
	description =  db.Column(db.String(512))
	imageurl =  db.Column(db.String(112))

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __init__(self,user_id,name,surname,birthdate,website,address,telephone,description,imageurl):
		self.user_id=user_id
		self.name=name
		self.surname=surname
		date_parts = [int(x) for x in birthdate.split('/')]
		self.birthdate = date(date_parts[2],date_parts[1],date_parts[0])
		self.birthdate=birthdate
		self.website=website
		self.address=address
		self.telephone=telephone
		self.description=description
		self.imageurl=imageurl


class Message(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	user_to = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
	user_from = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
	message= db.Column(db.String(112))

	def as_dict(self):
		return {c.id: getattr(self, c.id) for c in self.__table__.columns}

	def __init__(self,user_to,user_from,message):
		self.user_to=user_to
		self.user_from=user_from
		self.message=message
