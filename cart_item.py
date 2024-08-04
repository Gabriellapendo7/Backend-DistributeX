from flask import Blueprint, request, jsonify
from app import db
from models import CartItem

cart_item_bp = Blueprint('cart_item_bp', __name__)

@cart_item_bp.route('/', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    return jsonify([cart_item.to_dict() for cart_item in cart_items])

@cart_item_bp.route('/<int:id>', methods=['GET'])
def get_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    return jsonify(cart_item.to_dict())

@cart_item_bp.route('/', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    new_cart_item = CartItem(
        CartID=data['CartID'],
        ProductID=data['ProductID'],
        quantity=data['quantity']
    )
    db.session.add(new_cart_item)
    db.session.commit()
    return jsonify(new_cart_item.to_dict()), 201

@cart_item_bp.route('/<int:id>', methods=['PUT'])
def update_cart_item(id):
    data = request.get_json()
    cart_item = CartItem.query.get_or_404(id)
    cart_item.CartID = data['CartID']
    cart_item.ProductID = data['ProductID']
    cart_item.quantity = data['quantity']
    db.session.commit()
    return jsonify(cart_item.to_dict())

@cart_item_bp.route('/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return '', 204
