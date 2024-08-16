from flask import Blueprint, request, jsonify
from config import db
from models import Supply  
from datetime import datetime
import logging

supply_bp = Blueprint('supply', __name__)

@supply_bp.route('', methods=['POST'])
def add_supply():
    logging.info("Received request to add supply.")
    
    data = request.get_json()

    if not all(key in data for key in ('supply_name', 'quantity_ordered', 'order_date')):
        return jsonify({'message': 'Missing data'}), 400

    try:
        order_date = datetime.strptime(data['order_date'], "%Y-%m-%d")

        new_supply = Supply(
            supply_name=data['supply_name'],
            quantity_ordered=data['quantity_ordered'],
            order_date=order_date
        )

        db.session.add(new_supply)
        db.session.commit()

        return jsonify({'message': 'Supply added successfully', 'supply': new_supply.ID}), 201
    
    except Exception as e:
        logging.error(f"Error adding supply: {e}")
        return jsonify({'message': 'An error occurred while adding the supply.'}), 500

@supply_bp.route('', methods=['GET'])
def get_supplies():
    logging.info("Received request to get supplies.")
    
    try:
        supplies = Supply.query.all()
        supplies_list = [{
            'ID': supply.ID,
            'supply_name': supply.supply_name,
            'quantity_ordered': supply.quantity_ordered,
            'order_date': supply.order_date.strftime("%Y-%m-%d")
        } for supply in supplies]

        return jsonify(supplies_list), 200
    
    except Exception as e:
        logging.error(f"Error retrieving supplies: {e}")
        return jsonify({'message': 'An error occurred while retrieving the supplies.'}), 500

@supply_bp.route('/<int:supply_id>', methods=['PUT'])
def update_supply(supply_id):
    logging.info(f"Received request to update supply with ID: {supply_id}.")
    
    data = request.get_json()

    if not all(key in data for key in ('supply_name', 'quantity_ordered', 'order_date')):
        return jsonify({'message': 'Missing data'}), 400

    try:
        supply = Supply.query.get(supply_id)
        if not supply:
            return jsonify({'message': 'Supply not found'}), 404

        supply.supply_name = data['supply_name']
        supply.quantity_ordered = data['quantity_ordered']
        supply.order_date = datetime.strptime(data['order_date'], "%Y-%m-%d")
        
        db.session.commit()

        return jsonify({
            'message': 'Supply updated successfully',
            'supply': {
                'ID': supply.ID,
                'supply_name': supply.supply_name,
                'quantity_ordered': supply.quantity_ordered,
                'order_date': supply.order_date.strftime("%Y-%m-%d")
            }
        }), 200

    except Exception as e:
        logging.error(f"Error updating supply: {e}")
        return jsonify({'message': 'An error occurred while updating the supply.'}), 500
