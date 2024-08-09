from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config, db, ma, migrate, bcrypt
from routes.manufacturerAuth import manufacturer_auth_bp 

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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
