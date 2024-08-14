from flask import Blueprint, make_response, request
from flask_restful import Resource
from models import Category
from config import db
from helpers import commit_session, validate_not_blank  

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return make_response([category.to_dict() for category in categories], 200)

@categories_bp.route('/categories', methods=['POST'])
def create_category():
    category_data = request.get_json()
    name = category_data.get("name")

    try:
        validate_not_blank(name, "name")
        new_category = Category(name=name)
        db.session.add(new_category)
        commit_session(db.session)
        return make_response({"message": "Category created successfully"}, 201)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": "Failed to create category: " + str(e)}, 500)
