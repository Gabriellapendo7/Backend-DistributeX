from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from models import User  # Import your User model
from app import db  # Import your database instance

# Create a Blueprint
clients_bp = Blueprint('clients_api', __name__)
api = Api(clients_bp)

# Define a Resource to handle fetching users
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

# Add the resource to the API
api.add_resource(UserListResource, '/clients')
