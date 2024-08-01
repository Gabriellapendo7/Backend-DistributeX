from flask import Blueprint, jsonify, request  
from models import db  
from models import Manufacturer  

manufacturers_bp = Blueprint('manufacturers', __name__)  

@manufacturers_bp.route('/manufacturers', methods=['POST'])  
def add_manufacturer():  
    data = request.get_json()  
    new_manufacturer = Manufacturer(name=data['name'])  
    db.session.add(new_manufacturer)  
    db.session.commit()  
    return jsonify({"message": "Manufacturer added"}), 201