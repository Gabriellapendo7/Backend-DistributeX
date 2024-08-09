from flask import Blueprint, request, jsonify
from config import db
from models import Supply  # Ensure this import matches your models file structure

supply_bp = Blueprint('supply', __name__)

@supply_bp.route('/api/supply', methods=['POST'])
def add_supply():
    # Get data from the request
    data = request.get_json()

    # Validate input data (You can add more validation as needed)
    if not all(key in data for key in ('AdminID', 'ManufacturerID', 'supply_name', 'quantity_ordered', 'order_date', 'ProductID')):
        return jsonify({'message': 'Missing data'}), 400

    # Create a new Supply instance
    new_supply = Supply(
        AdminID=data['AdminID'],
        ManufacturerID=data['ManufacturerID'],
        supply_name=data['supply_name'],
        quantity_ordered=data['quantity_ordered'],
        order_date=data['order_date'],
        ProductID=data['ProductID']
    )

    # Add the supply to the database
    db.session.add(new_supply)
    db.session.commit()

    return jsonify({'message': 'Supply added successfully', 'supply': new_supply.ID}), 201
