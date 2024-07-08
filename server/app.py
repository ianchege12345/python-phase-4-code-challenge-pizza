from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

# Define routes

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    response = make_response(
        jsonify([restaurant.to_dict() for restaurant in restaurants]),
        200
    )
    return response

# GET /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        response = make_response(
            jsonify({"error": "Restaurant not found"}),
            404
        )
        return response

    response = make_response(
        jsonify(restaurant.to_dict()),
        200
    )
    return response

# DELETE /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        response = make_response(
            jsonify({"error": "Restaurant not found"}),
            404
        )
        return response

    db.session.delete(restaurant)
    db.session.commit()
    response = make_response(
        '',
        204
    )
    return response

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    response = make_response(
        jsonify([pizza.to_dict() for pizza in pizzas]),
        200
    )
    return response

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Validate input
    errors = []
    if not price or not isinstance(price, (float, int)) or not (1 <= price <= 30):
        errors.append('Price must be a number between 1 and 30')
    if not Pizza.query.get(pizza_id):
        errors.append('Pizza not found')
    if not Restaurant.query.get(restaurant_id):
        errors.append('Restaurant not found')

    if errors:
        response = make_response(
            jsonify({'errors': errors}),
            400
        )
        return response

    # Create RestaurantPizza
    restaurant_pizza = RestaurantPizza(
        price=price,
        pizza_id=pizza_id,
        restaurant_id=restaurant_id
    )
    db.session.add(restaurant_pizza)
    db.session.commit()

    response = make_response(
        jsonify(restaurant_pizza.to_dict(include={'pizza', 'restaurant'})),
        201
    )
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5555)
