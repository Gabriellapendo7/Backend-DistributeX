from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from models import Product
from helpers import commit_session
from config import db

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = [
            product.to_dict(convert_price_to_dollars=True) for product in Product.query.all()
        ]
        return make_response({"products": products}, 200)
    except Exception as error:
        return make_response({"error": str(error)}, 500)

@products_bp.route('/products', methods=['POST'])
def create_product():
    product_data = request.get_json()
    try:
        required_fields = [
            "name",
            "description",
            "price",
            "item_quantity",
            "image_url",
            "imageAlt",
        ]
        if not all(field in product_data for field in required_fields):
            return make_response({"error": "Missing required fields"}, 400)

        # Convert price to cents
        new_product_price = int(float(product_data["price"]) * 100)

        new_product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=new_product_price,
            item_quantity=product_data["item_quantity"],
            image_url=product_data["image_url"],
            imageAlt=product_data["imageAlt"],
        )
        db.session.add(new_product)
        commit_session(db.session)
        return make_response({"new_product": new_product.to_dict()}, 201)
    except IntegrityError:
        return make_response(
            {"error": "Product creation failed due to a database error."}, 400
        )
    except Exception as error:
        return make_response({"error": str(error)}, 500)

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    if product:
        return make_response(product.to_dict(convert_price_to_dollars=True), 200)
    else:
        return make_response({"error": "Product not found"}, 404)

@products_bp.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    product = Product.query.get(id)
    if product:
        data = request.get_json()
        try:
            for attr in data:
                setattr(product, attr, data[attr])
            commit_session(db.session)
            return make_response(product.to_dict(), 202)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
    else:
        return make_response({"error": "Product not found"}, 404)

@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            commit_session(db.session)
            return jsonify({}), 204
        else:
            return make_response({"error": "Product not found"}), 404
    except Exception as error:
        return make_response({"error": str(error)}, 500)
