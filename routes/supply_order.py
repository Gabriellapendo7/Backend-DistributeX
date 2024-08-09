from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from config import db
from models import SupplyOrder, Product

supply_order_bp = Blueprint('supply_order', __name__)
api = Api(supply_order_bp)

class SupplyOrderResource(Resource):
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

class SupplyOrderResource(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            delivery_schedule = datetime.fromisoformat(data['delivery_schedule'].replace('Z', '+00:00'))
        except ValueError:
            return {'message': 'Invalid date format'}, 400

        supply_order = SupplyOrder(
            contact_information=data['contact_information'],
            delivery_schedule=delivery_schedule,
            pricing_and_payment=data['pricing_and_payment'],
            shipping_information=data['shipping_information'],
            product_information=data['product_information'],
            order_details=data['order_details'],
            ProductID=data['ProductID']
        )

        db.session.add(supply_order)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'Supply order created successfully'}, 201
    def put(self, id):
        data = request.get_json()
        supply_order = SupplyOrder.query.get(id)

        if not supply_order:
            return {'message': 'Supply Order not found'}, 404

        supply_order.contact_information = data['contact_information']
        supply_order.delivery_schedule = data['delivery_schedule']
        supply_order.pricing_and_payment = data['pricing_and_payment']
        supply_order.shipping_information = data['shipping_information']
        supply_order.product_information = data['product_information']
        supply_order.order_details = data['order_details']
        supply_order.ProductID = data['ProductID']

        db.session.commit()

        return {'message': 'Supply Order updated'}

    def delete(self, id):
        supply_order = SupplyOrder.query.get(id)

        if not supply_order:
            return {'message': 'Supply Order not found'}, 404

        db.session.delete(supply_order)
        db.session.commit()

        return {'message': 'Supply Order deleted'}

api.add_resource(SupplyOrderResource, '/supply_orders', '/supply_orders/<int:id>')
