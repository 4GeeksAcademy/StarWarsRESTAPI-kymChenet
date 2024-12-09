from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
  
    favorites = db.relationship( "Favorite", backref="user")
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
           "favorite": [fav.serialize() for fav in self.favorite]
        }

class Planet(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }

class People(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(20), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)

    planet = db.relationshio("Planet")
    people = db.relationshio("People")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            # do not serialize the password, its a security breach
        }