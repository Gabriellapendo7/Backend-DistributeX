from flask import Blueprint, request, jsonify
from app import db
from models import Cart

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return jsonify([cart.to_dict() for cart in carts])

@cart_bp.route('/<int:id>', methods=['GET'])
def get_cart(id):
    cart = Cart.query.get_or_404(id)
    return jsonify(cart.to_dict())

@cart_bp.route('/', methods=['POST'])
def create_cart():
    data = request.get_json()
    new_cart = Cart(
        ClientID=data['ClientID']
    )
    db.session.add(new_cart)
    db.session.commit()
    return jsonify(new_cart.to_dict()), 201

@cart_bp.route('/<int:id>', methods=['PUT'])
def update_cart(id):
    data = request.get_json()
    cart = Cart.query.get_or_404(id)
    cart.ClientID = data['ClientID']
    db.session.commit()
    return jsonify(cart.to_dict())

@cart_bp.route('/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get_or_404(id)
    db.session.delete(cart)
    db.session.commit()
    return '', 204
