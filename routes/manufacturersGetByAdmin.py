from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from config import db  
from models import Manufacturer

manufacturer_bp = Blueprint('manufacturer_api', __name__)
api = Api(manufacturer_bp)

class ManufacturerListResource(Resource):
    def get(self):
        manufacturers = Manufacturer.query.all()
        return jsonify([manufacturer.to_dict() for manufacturer in manufacturers])

api.add_resource(ManufacturerListResource, '/manufacturers')
