from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return '<h1>Plant Store API is Running!</h1>'

# GET /plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

# GET /plants/<id>
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict())

# POST /plants
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()

    if not all(field in data for field in ('name', 'image', 'price')):
        return {"error": "Missing fields in request"}, 400

    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=float(data['price'])
    )

    db.session.add(new_plant)
    db.session.commit()

    return jsonify(new_plant.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
