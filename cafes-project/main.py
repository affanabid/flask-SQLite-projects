from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    with app.app_context():
        db.create_all()

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
    
@app.route("/")
def home():
    return render_template("index.html")

## HTTP GET - Read Record
@app.route('/random')
def random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(random_cafe.to_dict())

@app.route('/all')
def all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify([cafe.to_dict() for cafe in all_cafes])

@app.route('/search')
def search():
    query_location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify([cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
## HTTP POST - Create Record
@app.route('/add')
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:id>')
def update_price(id):
    cafe = db.get_or_404(Cafe, id)
    new_price = request.args.get('new_price')
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "successfuly updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry, we can not find any cafe with this id in the database."})

## HTTP DELETE - Delete Record
@app.route('/report-closed/<id>')
def delete_cafe(id):
    key = 'password'
    cafe = db.get_or_404(Cafe, id)
    if cafe:
        api_key = request.args.get('api_key')
        if api_key == key:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success": "successfuly deleted the entry."})
        else:
            return jsonify(error={"Incorrect key": "Sorry, that's not allowd. Make sure you enter the correct key"})
    else:
        return jsonify(error={"Not Found": "Sorry, we can not find any cafe with this id in the database."})

if __name__ == '__main__':
    app.run(debug=True)
