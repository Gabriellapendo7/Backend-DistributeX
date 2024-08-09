from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from config import db
from models import SupplyOrder

supply_order_bp = Blueprint('supply_order', __name__)
api = Api(supply_order_bp)

class SupplyOrderGet(Resource):
    def get(self, id):
        supply_order = SupplyOrder.query.get(id)
        if not supply_order:
            return {'message': 'Supply Order not found'}, 404

        return {
            'ID': supply_order.ID,
            'contact_information': supply_order.contact_information,
            'delivery_schedule': supply_order.delivery_schedule.isoformat(),
            'pricing_and_payment': supply_order.pricing_and_payment,
            'shipping_information': supply_order.shipping_information,
            'product_information': supply_order.product_information,
            'order_details': supply_order.order_details,
            'ProductID': supply_order.ProductID
        }

class SupplyOrderPost(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'error': 'Invalid data format. Expected JSON object.'}, 400

            # Convert delivery_schedule from ISO format with 'Z' to a datetime object
            try:
                delivery_schedule = datetime.fromisoformat(data.get('delivery_schedule', '').replace('Z', '+00:00'))
            except ValueError as e:
                return {'error': f'Invalid date format: {e}'}, 400

            # Create a new SupplyOrder instance
            new_order = SupplyOrder(
                contact_information=data.get('contact_information'),
                delivery_schedule=delivery_schedule,
                pricing_and_payment=data.get('pricing_and_payment'),
                shipping_information=data.get('shipping_information'),
                product_information=data.get('product_information'),
                order_details=data.get('order_details'),
                ProductID=data.get('ProductID')
            )
            db.session.add(new_order)
            db.session.commit()

            return {'message': 'Supply order created successfully!', 'order': new_order.ID}, 201

        except Exception as e:
            return {'error': str(e)}, 500


            
class SupplyOrderDelete(Resource):
    def delete(self, id):
        supply_order = SupplyOrder.query.get(id)

        if not supply_order:
            return {'message': 'Supply Order not found'}, 404

        db.session.delete(supply_order)
        db.session.commit()

        return {'message': 'Supply Order deleted'}, 200

api.add_resource(SupplyOrderGet, '/supply_orders/<int:id>')
api.add_resource(SupplyOrderPost, '/supply_orders')
api.add_resource(SupplyOrderDelete, '/supply_orders/<int:id>')
