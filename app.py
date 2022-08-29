import json
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify


from models import *



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST',])
def get_users():
    if request.method == 'GET':
        result = []
        for user in User.query.all():
            result.append(User.users_dict(user))
        return jsonify(result)
      
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return 'Пользователь добавлен'

@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
     if request.method == 'GET':
        result = []
        for order in Order.query.all():
            result.append(Order.orders_dict(order))
        return jsonify(result)


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        result = []
        for offer in Offer.query.all():
            result.append(Offer.offers_dict(offer))
        return jsonify(result)


@app.route('/users/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        user = User.query.get(id)
        if user is None:
            return "Такого пользователя нет"
        else:
            return jsonify(User.users_dict(user)) 
    
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(id)
        if user is None:
            return "Такого пользователя, не существует"
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        return f"Пользователь с id {id} успешно изменён"
    elif request.method == 'DELETE':
        user = db.session.query(User).get(id)
        if user is None:
            return "Такого пользователя, не существует"
        db.session.delete(user)
        db.session.commit()
        return f"Пользователь с id {id} успешно удалён"
        
@app.route('/orders/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_order(id):
    if request.method == 'GET':
        order = Order.query.get(id)
        if order is None:
            return "Такого заказа нет"
        else:
            return jsonify(Order.orders_dict(order))

    elif request.method == 'PUT':      
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(id)
        month_start, day_start, year_start = order_data['start_date'].split('/')    
        month_end, day_end, year_end = order_data['end_date'].split('/')
        if order is None:
            return "Такого заказа, не существует"
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
        order.end_date = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return f"заказ с id {id} успешно изменён"
    elif request.method == 'DELETE':
        order = db.session.query(Order).get(id)
        if order is None:
            return "Такого заказа, не существует"
        db.session.delete(order)
        db.session.commit()
        return f"заказ с id {id} успешно удалён"

@app.route('/offers/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_offer(id):
    if request.method == 'GET':
        offer = Offer.query.get(id)
        if offer is None:
            return "Такого пользователя нет"
        else:
            return jsonify(Offer.offers_dict(offer))

    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(id)
        if offer is None:
            return "Такого предложения, не существует"
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.commit()
        return f"предложение с id {id} успешно изменён"
    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(id)
        if offer is None:
            return "Такого предложения, не существует"
        db.session.delete(offer)
        db.session.commit()
        return f"предложение с id {id} успешно удалён"
    
if __name__ == '__main__':
    app.run(debug=True)

