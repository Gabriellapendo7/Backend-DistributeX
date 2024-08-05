from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '2a471f3357ce40230b9f670bd05ec405384d502a70bbc3bf98d4509f4620e96a'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import models after setting up db and app
from app import Admin, Sales, Product, Order, SupplyOrder

# Create the database tables within the app context
with app.app_context():
    db.create_all()

    # Seed data for Admin
    admin1 = Admin(username='admin1', password=bcrypt.generate_password_hash('123').decode('utf-8'))
    admin2 = Admin(username='admin2', password=bcrypt.generate_password_hash('123').decode('utf-8'))

    # Seed data for Products
    product1 = Product(name='Product1', description='Description for product 1', price=10.99, stock=100)
    product2 = Product(name='Product2', description='Description for product 2', price=20.99, stock=200)
    product3 = Product(name='Product3', description='Description for product 3', price=30.99, stock=300)

    # Seed data for Orders
    order1 = Order(client_id=1, order_date=datetime.utcnow(), status='Pending', total_amount=100.50)
    order2 = Order(client_id=2, order_date=datetime.utcnow(), status='Shipped', total_amount=200.75)

    # Seed data for Sales
    sale1 = Sales(receipt_id='R001', admin_id=1, total_amount=100.50, client_id=1, sale_date=datetime.utcnow())
    sale2 = Sales(receipt_id='R002', admin_id=2, total_amount=200.75, client_id=2, sale_date=datetime.utcnow())

    # Seed data for SupplyOrders
    supply_order1 = SupplyOrder(order_id=1, product_id=1, quantity=10, price=10.99, order_date=datetime.utcnow())
    supply_order2 = SupplyOrder(order_id=2, product_id=2, quantity=20, price=20.99, order_date=datetime.utcnow())

    # Add all seed data to the session
    db.session.add(admin1)
    db.session.add(admin2)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)

    db.session.add(order1)
    db.session.add(order2)

    db.session.add(sale1)
    db.session.add(sale2)

    db.session.add(supply_order1)
    db.session.add(supply_order2)

    # Commit the session
    db.session.commit()

    print("Database seeded!")
