from flask import Blueprint, request
from flask_restful import Api, Resource
from models import db, Product 

admin_products_bp = Blueprint('admin_products_bp', __name__)
api = Api(admin_products_bp)

class ProductAPI(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return product.to_dict(convert_price_to_dollars=True), 200
            return {"error": "Product not found"}, 404
        else:
            products = Product.query.all()
            return [product.to_dict(convert_price_to_dollars=True) for product in products], 200

    def post(self):
        data = request.json
        try:
            new_product = Product(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                item_quantity=data.get('item_quantity', 0),
                image_url=data.get('image_url'),
                imageAlt=data.get('imageAlt')
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product.to_dict(convert_price_to_dollars=True), 201
        except Exception as e:
            return {"error": str(e)}, 400

    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.json
        try:
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.item_quantity = data.get('item_quantity', product.item_quantity)
            product.image_url = data.get('image_url', product.image_url)
            product.imageAlt = data.get('imageAlt', product.imageAlt)
            
            db.session.commit()
            return product.to_dict(convert_price_to_dollars=True), 200
        except Exception as e:
            return {"error": str(e)}, 400

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400


api.add_resource(ProductAPI, '/products', '/products/<int:product_id>')
