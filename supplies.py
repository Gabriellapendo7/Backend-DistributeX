from flask import Blueprint, jsonify, request  
from models import db  
from models import Supply  

supplies_bp = Blueprint('supplies', __name__)  

@supplies_bp.route('/supplies', methods=['POST'])  
def add_supply():  
    data = request.get_json()  
    new_supply = Supply(product_id=data['product_id'], quantity=data['quantity'])  
    db.session.add(new_supply)  
    db.session.commit()  
    return jsonify({"message": "Supply added"}), 201