from flask import Flask
from extensions import db, migrate
from manufacturers import manufacturers_bp
from products import products_bp
from supplies import supplies_bp
from supply_orders import supply_orders_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///distributex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db.init_app(app)
migrate.init_app(app, db)

# Register Blueprints
app.register_blueprint(manufacturers_bp)
app.register_blueprint(products_bp)
app.register_blueprint(supplies_bp)
app.register_blueprint(supply_orders_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
