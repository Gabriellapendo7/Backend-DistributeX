from flask import Blueprint, make_response, request
from models import ProductCategory
from config import db  
from helpers import commit_session, validate_type  

product_categories_bp = Blueprint('product_categories', __name__)

@product_categories_bp.route('/product_categories', methods=['GET'])
def get_product_categories():
    product_categories = ProductCategory.query.all()
    return make_response([product_category.to_dict() for product_category in product_categories], 200)

@product_categories_bp.route('/product_categories', methods=['POST'])
def create_product_category():
    data = request.get_json()
    product_id = data.get("product_id")
    category_id = data.get("category_id")

    try:
        validate_type(product_id, "product_id", int)
        validate_type(category_id, "category_id", int)

        new_product_category = ProductCategory(
            product_id=product_id, category_id=category_id
        )
        db.session.add(new_product_category)
        commit_session(db.session)
        return make_response({"message": "ProductCategory created successfully"}, 201)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": "Failed to create product category: " + str(e)}, 500)
