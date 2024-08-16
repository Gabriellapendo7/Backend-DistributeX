from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from config import db
from models import Product

admin_products_bp = Blueprint('admin_products_bp', __name__)
api = Api(admin_products_bp)

class ProductResource(Resource):
    def options(self):
        return jsonify({'message': 'Preflight response'})

    def get(self):
        products = Product.query.all()
        products_list = [{
            'id': product.id,
            'productName': product.productName,
            'description': product.description,
            'price': product.price,
            'itemQuantity': product.itemQuantity,
            'contactInfo': product.contactInfo,
            'manufacturer_id': product.manufacturer_id
        } for product in products]
        return jsonify({'products': products_list})

    def post(self):
        data = request.get_json()
        print("Received product data:", data)
        required_fields = ['productName', 'price', 'itemQuantity']

        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        try:
            new_product = Product(
                productName=data['productName'],
                description=data.get('description', ''),  
                price=data['price'],
                itemQuantity=data['itemQuantity'],
                contactInfo=data.get('contactInfo', ''),  
                manufacturer_id=data.get('manufacturer_id', 1)  
            )
            db.session.add(new_product)
            db.session.commit()
            return jsonify({"message": "Product added successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400


    def patch(self, product_id):
        data = request.get_json()
        try:
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"message": "Product not found"}), 404

            product.productName = data.get('productName', product.productName)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.itemQuantity = data.get('itemQuantity', product.itemQuantity)
            product.contactInfo = data.get('contactInfo', product.contactInfo)
            product.manufacturer_id = data.get('manufacturer_id', product.manufacturer_id)

            db.session.commit()
            return jsonify({"message": "Product updated successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400

    def delete(self, product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"message": "Product not found"}), 404

            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400

api.add_resource(ProductResource, '/', '/<int:product_id>')
