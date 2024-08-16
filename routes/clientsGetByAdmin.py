from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from models import db, Manufacturer  # Import from models

clients_bp = Blueprint('clients_bp', __name__)
api = Api(clients_bp)

class ClientListResource(Resource):
    def get(self):
        try:
            # Assuming you have a Client model
            clients = db.session.query(Client).all()
            return jsonify([client.to_dict() for client in clients])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

api.add_resource(ClientListResource, '/clients')
