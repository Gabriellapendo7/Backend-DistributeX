from flask import Blueprint, jsonify, request  
from models import db  
from models import SupplyOrder  

supply_orders_bp = Blueprint('supply_orders', __name__)  

@supply_orders_bp.route('/supply-orders', methods=['POST'])  
def add_supply_order():  
    data = request.get_json()  
    new_supply_order = SupplyOrder(supply_id=data['supply_id'], order_date=data['order_date'])  
    db.session.add(new_supply_order)  
    db.session.commit()  
    return jsonify({"message": "Supply order placed"}), 201