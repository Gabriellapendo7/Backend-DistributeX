from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from config import db
from models import Manufacturer

manufacturersGetByAdmin_bp = Blueprint('manufacturersGetByAdmin_bp', __name__)
api = Api(manufacturersGetByAdmin_bp)

class ManufacturerListResource(Resource):
    def get(self):
        manufacturers = Manufacturer.query.all()
        return jsonify([manufacturer.to_dict() for manufacturer in manufacturers])

# Add the resource to the API
api.add_resource(ManufacturerListResource, '/')

