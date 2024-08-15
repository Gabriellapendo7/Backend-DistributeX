from flask import Flask
from flask_cors import CORS
from config import Config, db, ma, migrate, bcrypt

# Import blueprints from the routes folder
from routes.products import products_bp
from routes.users import users_bp
from routes.orders import orders_bp
from routes.categories import categories_bp
from routes.product_categories import product_categories_bp
from routes.login import login_bp
from routes.manufacturer import manufacturer_bp
from routes.adminProducts import admin_products_bp
from routes.clientsGetByAdmin import clients_bp
from routes.adminManufacturerOrders import adminManufacturerOrders_bp

def create_app():
    app = Flask(__name__, static_folder="../client/src/assets", static_url_path="/assets")
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints with URL prefixes
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(product_categories_bp, url_prefix='/api/product-categories')
    app.register_blueprint(login_bp, url_prefix='/api/login')
    app.register_blueprint(manufacturer_bp, url_prefix='/api/manufacturers')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(admin_products_bp, url_prefix='/admin/products')
    app.register_blueprint(adminManufacturerOrders_bp, url_prefix='/admin/orders')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
