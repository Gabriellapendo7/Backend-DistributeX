from flask import Blueprint, make_response, request
from models import Order, OrderDetail
from config import db
from helpers import commit_session  

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return make_response([order.to_dict() for order in orders], 200)
    except Exception as error:
        return make_response({"error": str(error)}, 500)

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    try:
        new_order = Order(user_id=order_data["user_id"])
        db.session.add(new_order)
        db.session.flush()

        for detail in order_data["order_details"]:
            order_detail = OrderDetail(
                order_id=new_order.id,
                product_id=detail["product_id"],
                quantity=detail["quantity"],
            )
            db.session.add(order_detail)

        commit_session(db.session)
        return make_response({"message": "Order created successfully"}, 201)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": "Order creation failed: " + str(e)}, 500)
