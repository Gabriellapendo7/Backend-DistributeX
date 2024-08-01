from flask import Blueprint, jsonify, request  
from models import db  
from models import Product  

products_bp = Blueprint('products', __name__)  

@products_bp.route('/products', methods=['POST'])  
def add_product():  
    data = request.get_json()  
    new_product = Product(name=data['name'], manufacturer_id=data['manufacturer_id'])  
    db.session.add(new_product)  
    db.session.commit()  
    return jsonify({"message": "Product added"}), 201