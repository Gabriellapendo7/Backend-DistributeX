from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from config import db
from models import SupplyOrder

supply_order_bp = Blueprint('supply_order', __name__)
api = Api(supply_order_bp)

class SupplyOrderList(Resource):
    def get(self):
        supply_orders = SupplyOrder.query.all()

        result = [order.to_dict() for order in supply_orders]
        return result, 200

class SupplyOrderGet(Resource):
    def get(self, id):

        supply_order = SupplyOrder.query.get(id)
        if not supply_order:
            return {'message': 'Supply Order not found'}, 404
        return supply_order.to_dict(), 200

class SupplyOrderPost(Resource):
    def post(self):
        data = request.get_json()

        delivery_schedule = datetime.fromisoformat(data.get('delivery_schedule', '').replace('Z', '+00:00'))
        new_order = SupplyOrder(**data, delivery_schedule=delivery_schedule)
        db.session.add(new_order)
        db.session.commit()
        return {'message': 'Supply order created successfully!', 'order': new_order.ID}, 201

class SupplyOrderDelete(Resource):
    def delete(self, id):
        supply_order = SupplyOrder.query.get(id)
        if not supply_order:
            return {'message': 'Supply Order not found'}, 404
        db.session.delete(supply_order)
        db.session.commit()
        return {'message': 'Supply Order deleted'}, 200


api.add_resource(SupplyOrderList, '/supply_orders')
api.add_resource(SupplyOrderGet, '/supply_orders/<int:id>')
api.add_resource(SupplyOrderPost, '/supply_orders')
api.add_resource(SupplyOrderDelete, '/supply_orders/<int:id>')
