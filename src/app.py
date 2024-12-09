"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    result = [user.serialize() for user in users]

    response_body = {
        "users": result
    }

    return jsonify(response_body), 200





@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()
    result = [person.serialize() for person in people]

    return jsonify(result), 200





@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    person = People.query.get(people_id)
    if not person: 
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person.serialize()), 200





@app.route('/planets/', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200





@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):

    planet = Planet.query.get(planet_id)
    if not planet: 
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200






@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
     
    current_user_id = 1
    favorites = Favorites.query.filter_by(user_id=current_user_id).all()
    result = [fav.serialize() for fav in favorites]
    return jsonify(result), 200





@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
     
    current_user_id = 1
    planet = Planet.query.get(planet_id)
    if not planet: 
      return jsonify({"error": "Planet not found"}), 404
    
    new_favorite = Favorites(user_id=current_user_id, planet_id=planet_id, people_id=None)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201





@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):

    current_user_id = 1
    person = People.query.get(people_id)
    if not person: 
      return jsonify({"error": "Person not found"}), 404
    
    new_favorite = Favorites(user_id=current_user_id, planet_id=None, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201





@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
     
    current_user_id = 1
    favorite = Favorites.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite: 
      return jsonify({"error": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 201




@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
     
    current_user_id = 1
    favorite = Favorites.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if not favorite: 
      return jsonify({"error": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
