from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config, db, ma, migrate, bcrypt
from routes.manufacturerAuth import manufacturer_auth_bp 
from routes.supply import supply_bp 
from routes.supply_order import supply_order_bp 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    api = Api(app)

    app.register_blueprint(manufacturer_auth_bp)  
    app.register_blueprint(supply_bp)
    app.register_blueprint(supply_order_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
