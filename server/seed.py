from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '2a471f3357ce40230b9f670bd05ec405384d502a70bbc3bf98d4509f4620e96a'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
faker = Faker()

# Models start here
class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Sales(db.Model):
    __tablename__ = 'sales'
    sales_id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
# Models end here

# Faker data generation
def create_fake_data():
    # Create fake Admins
    for _ in range(5):
        hashed_password = bcrypt.generate_password_hash(faker.password()).decode('utf-8')
        new_admin = Admin(
            username=faker.user_name(),
            password=hashed_password
        )
        db.session.add(new_admin)

    # Create fake Products
    for _ in range(20):
        new_product = Product(
            name=faker.word(),
            description=faker.sentence(),
            price=round(faker.random_number(digits=2), 2),
            stock=faker.random_int(min=1, max=100)
        )
        db.session.add(new_product)

    db.session.commit()

    # Create fake Sales and Orders
    admins = Admin.query.all()
    products = Product.query.all()
    
    for _ in range(50):
        admin = faker.random_element(admins)
        new_sale = Sales(
            receipt_id=faker.uuid4(),
            admin_id=admin.admin_id,
            total_amount=round(faker.random_number(digits=2), 2),
            client_id=faker.random_int(min=1, max=1000),
            sale_date=faker.date_time_this_year()
        )
        db.session.add(new_sale)
    
    for _ in range(30):
        new_order = Order(
            client_id=faker.random_int(min=1, max=1000),
            order_date=faker.date_time_this_year(),
            status=faker.random_element(elements=('Pending', 'Shipped', 'Delivered')),
            total_amount=round(faker.random_number(digits=2), 2)
        )
        db.session.add(new_order)
    
    db.session.commit()

    orders = Order.query.all()
    
    for _ in range(100):
        order = faker.random_element(orders)
        product = faker.random_element(products)
        new_order_item = OrderItem(
            order_id=order.order_id,
            product_id=product.product_id,
            quantity=faker.random_int(min=1, max=10),
            price=round(product.price * faker.random_int(min=1, max=10), 2)
        )
        db.session.add(new_order_item)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_fake_data()
        print("Fake data created successfully!")
