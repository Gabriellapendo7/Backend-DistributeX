from flask import Flask  
# from config import Config  
from flask_migrate import Migrate
from models import db 
from manufacturers import manufacturers_bp  
from products import products_bp  
from supplies import supplies_bp  
from supply_orders import supply_orders_bp  

  
app = Flask(__name__)  
# app.config.from_object(Config)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Manufacturer.db'

  # Initialize the database  
db.init_app(app)  

    # Register Blueprints  
app.register_blueprint(manufacturers_bp)  
app.register_blueprint(products_bp)  
app.register_blueprint(supplies_bp)  
app.register_blueprint(supply_orders_bp)  


# Initialize extensions

migrate = Migrate(app=app, db=db)

if __name__ == '__main__':  
    app.run(debug=True)