from flask import Blueprint, request, jsonify
from config import db
from models import Supply  
import logging

supply_bp = Blueprint('supply', __name__)

@supply_bp.route('/api/supply', methods=['POST'])
def add_supply():
    logging.info("Received request to add supply.")
    
    data = request.get_json()

    # Ensure all necessary fields are present
    if not all(key in data for key in ('supply_name', 'quantity_ordered', 'order_date')):
        return jsonify({'message': 'Missing data'}), 400

    try:
        new_supply = Supply(
            supply_name=data['supply_name'],
            quantity_ordered=data['quantity_ordered'],
            order_date=data['order_date']  # Ensure order_date is a valid datetime string
        )

        db.session.add(new_supply)
        db.session.commit()

        return jsonify({'message': 'Supply added successfully', 'supply': new_supply.ID}), 201
    
    except Exception as e:
        logging.error(f"Error adding supply: {e}")
        return jsonify({'message': 'An error occurred while adding the supply.'}), 500
