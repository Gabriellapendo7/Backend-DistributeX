from flask import Blueprint, request
from flask_restful import Api, Resource
from models import db, Product
import traceback

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
        # Log the incoming data
        print("Received data for new product:", data)

        # Validation checks
        if 'name' not in data or 'description' not in data or 'price' not in data:
            print("Validation error: Missing required fields")
            return {"error": "Missing required fields"}, 400

        # Convert price from dollars to cents (assuming price is in dollars)
        try:
            price_in_cents = int(float(data['price']) * 100)
        except ValueError:
            print("Error converting price to cents")
            return {"error": "Invalid price format"}, 400

        new_product = Product(
            name=data.get('name'),
            description=data.get('description'),
            price=price_in_cents,
            item_quantity=data.get('item_quantity', 0),
            image_url=data.get('image_url'),
            imageAlt=data.get('imageAlt')
        )
        db.session.add(new_product)
        db.session.commit()
        print("Product added successfully:", new_product.to_dict(convert_price_to_dollars=True))
        return new_product.to_dict(convert_price_to_dollars=True), 201
    except Exception as e:
        print(f"Error occurred while adding product: {str(e)}")
        print(traceback.format_exc())
        return {"error": "An error occurred while processing your request."}, 500





    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.json
        try:
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)

            # Convert price from dollars to cents if provided
            if 'price' in data:
                product.price = int(float(data['price']) * 100)

            product.item_quantity = data.get('item_quantity', product.item_quantity)
            product.image_url = data.get('image_url', product.image_url)
            product.imageAlt = data.get('imageAlt', product.imageAlt)
            
            db.session.commit()
            return product.to_dict(convert_price_to_dollars=True), 200
        except Exception as e:
            print(f"Error occurred while updating product: {str(e)}")
            print(traceback.format_exc())
            return {"error": "An error occurred while processing your request."}, 500

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200
        except Exception as e:
            print(f"Error occurred while deleting product: {str(e)}")
            print(traceback.format_exc())
            return {"error": "An error occurred while processing your request."}, 500

api.add_resource(ProductAPI, '/products', '/products/<int:product_id>')
