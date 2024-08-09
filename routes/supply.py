from flask import Blueprint, request, jsonify
from config import db
from models import Supply  
from datetime import datetime
import logging

supply_bp = Blueprint('supply', __name__)

@supply_bp.route('/api/supply', methods=['POST'])
def add_supply():
    logging.info("Received request to add supply.")
    
    data = request.get_json()

    if not all(key in data for key in ('supply_name', 'quantity_ordered', 'order_date')):
        return jsonify({'message': 'Missing data'}), 400

    try:
        # Convert order_date from string to datetime object
        order_date = datetime.strptime(data['order_date'], "%Y-%m-%d")

        new_supply = Supply(
            supply_name=data['supply_name'],
            quantity_ordered=data['quantity_ordered'],
            order_date=order_date  # Use the converted datetime object
        )

        db.session.add(new_supply)
        db.session.commit()

        return jsonify({'message': 'Supply added successfully', 'supply': new_supply.ID}), 201
    
    except Exception as e:
        logging.error(f"Error adding supply: {e}")
        return jsonify({'message': 'An error occurred while adding the supply.'}), 500
