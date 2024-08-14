from flask import Blueprint, jsonify
from app import db
from models import Product, Review, Sales, Order, Client

routes = Blueprint('routes', __name__)

@routes.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [
        {
            'id': product.ID,
            'name': product.Productname,
            'price': product.price,
            'sales': len(product.order_details)  # Adjusted to reflect sales count correctly
        }
        for product in products
    ]
    return jsonify(product_list), 200

@routes.route('/api/sales', methods=['GET'])
def get_sales():
    sales = Sales.query.all()
    sales_data = [
        {
            'id': sale.ID,
            'total_amount': sale.TotalAmount,
            'sale_date': sale.Sale_date.strftime('%Y-%m-%d')
        }
        for sale in sales
    ]
    return jsonify(sales_data), 200

@routes.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = [
        {
            'id': review.ID,
            'user': review.client.Username,
            'comment': review.comment,
            'rating': review.rating
        }
        for review in reviews
    ]
    return jsonify(review_list), 200

@routes.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    client_list = [
        {
            'id': client.ID,
            'username': client.Username,
            'email': client.Email
        }
        for client in clients
    ]
    return jsonify(client_list), 200

@routes.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_list = [
        {
            'id': order.ID,
            'client_id': order.ClientID,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'status': order.status,
            'total': order.total
        }
        for order in orders
    ]
    return jsonify(order_list), 200



    
    
