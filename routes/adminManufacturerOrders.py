from flask import Blueprint, request, abort, jsonify
from flask_restful import Api, Resource
from models import db, ManufacturerProduct

adminManufacturerOrders_bp = Blueprint('adminManufacturerOrders_bp', __name__)
api = Api(adminManufacturerOrders_bp)

class ManufacturerProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = ManufacturerProduct.query.get(product_id)
            if not product:
                abort(404, description="Product not found")
            return jsonify(product.to_dict())
        else:
            products = ManufacturerProduct.query.all()
            return jsonify([product.to_dict() for product in products])

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, description="No input data provided")
        
        product_name = data.get('productName')
        if not product_name:
            abort(400, description="Missing or null value for field: productName")
        
        product = ManufacturerProduct(
            manufacturer_id=data.get('manufacturer_id'),
            product_name=product_name,
            description=data.get('description'),
            price=data.get('price'),
            item_quantity=data.get('itemQuantity'),
            admins_contact_info=data.get('contactInfo')
        )
        
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201

    def put(self, product_id):
        product = ManufacturerProduct.query.get(product_id)
        if not product:
            abort(404, description="Product not found")
        
        data = request.get_json()
        if not data:
            abort(400, description="No input data provided")

        product.product_name = data.get('productName', product.product_name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.item_quantity = data.get('itemQuantity', product.item_quantity)
        product.admins_contact_info = data.get('contactInfo', product.admins_contact_info)

        db.session.commit()
        return jsonify(product.to_dict())

    def delete(self, product_id):
        product = ManufacturerProduct.query.get(product_id)
        if not product:
            abort(404, description="Product not found")

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 204

api.add_resource(ManufacturerProductResource, '/products', '/products/<int:product_id>')
