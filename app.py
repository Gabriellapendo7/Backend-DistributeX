from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config, db, ma, migrate, bcrypt
from routes.products import products_bp
from routes.users import users_bp
from routes.orders import orders_bp
from routes.categories import categories_bp
from routes.product_categories import product_categories_bp
from routes.login import login_bp
from routes.manufacturer import manufacturer_bp

def create_app():
    app = Flask(__name__, static_folder="../client/src/assets", static_url_path="/assets")
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    api = Api(app)

    # Register blueprints
    app.register_blueprint(products_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(product_categories_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(manufacturer_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
