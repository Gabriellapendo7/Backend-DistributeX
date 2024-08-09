from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from config import db
from models import SupplyOrder

# Create a Blueprint for the supply order API
supply_order_bp = Blueprint('supply_order', __name__)
api = Api(supply_order_bp)

# Define the resource for handling the list of supply orders
class SupplyOrderList(Resource):
    def get(self):
        # Fetch all supply orders from the database
        supply_orders = SupplyOrder.query.all()
        # Convert each order to a dictionary format
        result = [order.to_dict() for order in supply_orders]
        return result, 200

# Define the resource for handling individual supply orders
class SupplyOrderGet(Resource):
    def get(self, id):
        # Fetch a specific supply order by ID
        supply_order = SupplyOrder.query.get(id)
        if not supply_order:
            return {'message': 'Supply Order not found'}, 404
        return supply_order.to_dict(), 200

# Define the resource for creating a new supply order
class SupplyOrderPost(Resource):
    def post(self):
        data = request.get_json()
        # Convert delivery_schedule from ISO format to a datetime object
        delivery_schedule = datetime.fromisoformat(data.get('delivery_schedule', '').replace('Z', '+00:00'))
        new_order = SupplyOrder(**data, delivery_schedule=delivery_schedule)
        # Add the new order to the database
        db.session.add(new_order)
        db.session.commit()
        return {'message': 'Supply order created successfully!', 'order': new_order.ID}, 201

# Define the resource for deleting a supply order
class SupplyOrderDelete(Resource):
    def delete(self, id):
        # Fetch a specific supply order by ID
        supply_order = SupplyOrder.query.get(id)
        if not supply_order:
            return {'message': 'Supply Order not found'}, 404
        # Delete the order from the database
        db.session.delete(supply_order)
        db.session.commit()
        return {'message': 'Supply Order deleted'}, 200

# Add resources to the API
api.add_resource(SupplyOrderList, '/supply_orders')
api.add_resource(SupplyOrderGet, '/supply_orders/<int:id>')
api.add_resource(SupplyOrderPost, '/supply_orders')
api.add_resource(SupplyOrderDelete, '/supply_orders/<int:id>')
