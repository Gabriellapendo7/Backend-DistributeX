from flask import Blueprint, jsonify
from app import db
from models import Product, Review, Sales, Order, Client, OrderDetails, Receipt, Cart, CartItem, Supply, SupplyOrder, Manufacturer, Category, Admin

routes = Blueprint('routes', __name__)

# Products
@routes.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [
        {
            'id': product.ID,
            'name': product.Productname,
            'price': product.price,
            'sales': len(product.order_details)
        }
        for product in products
    ]
    return jsonify(product_list), 200

# Reviews
@routes.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = [
        {
            'id': review.ID,
            'user': review.client.Username,
            'comment': review.comment,
            'rating': review.rating
        }
        for review in reviews
    ]
    return jsonify(review_list), 200

# Sales
@routes.route('/api/sales', methods=['GET'])
def get_sales():
    sales = Sales.query.all()
    sales_data = [
        {
            'id': sale.ID,
            'total_amount': sale.TotalAmount,
            'sale_date': sale.Sale_date.strftime('%Y-%m-%d')
        }
        for sale in sales
    ]
    return jsonify(sales_data), 200

# Orders
@routes.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_list = [
        {
            'id': order.ID,
            'client_id': order.ClientID,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'status': order.status,
            'total': order.total
        }
        for order in orders
    ]
    return jsonify(order_list), 200

# Order Details
@routes.route('/api/order_details', methods=['GET'])
def get_order_details():
    order_details = OrderDetails.query.all()
    order_details_list = [
        {
            'id': detail.ID,
            'order_id': detail.OrderID,
            'product_id': detail.ProductID,
            'quantity': detail.Quantity,
            'price': detail.Price
        }
        for detail in order_details
    ]
    return jsonify(order_details_list), 200

# Clients
@routes.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    client_list = [
        {
            'id': client.ID,
            'username': client.Username,
            'email': client.Email
        }
        for client in clients
    ]
    return jsonify(client_list), 200

# Receipts
@routes.route('/api/receipts', methods=['GET'])
def get_receipts():
    receipts = Receipt.query.all()
    receipt_list = [
        {
            'id': receipt.ID,
            'order_id': receipt.OrderID,
            'amount': receipt.Amount,
            'receipt_date': receipt.Receipt_date.strftime('%Y-%m-%d')
        }
        for receipt in receipts
    ]
    return jsonify(receipt_list), 200

# Carts
@routes.route('/api/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    cart_list = [
        {
            'id': cart.ID,
            'client_id': cart.ClientID,
            'total': cart.TotalAmount
        }
        for cart in carts
    ]
    return jsonify(cart_list), 200

# Cart Items
@routes.route('/api/cart_items', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    cart_item_list = [
        {
            'id': item.ID,
            'cart_id': item.CartID,
            'product_id': item.ProductID,
            'quantity': item.Quantity,
            'price': item.Price
        }
        for item in cart_items
    ]
    return jsonify(cart_item_list), 200

# Supplies
@routes.route('/api/supplies', methods=['GET'])
def get_supplies():
    supplies = Supply.query.all()
    supply_list = [
        {
            'id': supply.ID,
            'manufacturer_id': supply.ManufacturerID,
            'product_id': supply.ProductID,
            'quantity': supply.Quantity
        }
        for supply in supplies
    ]
    return jsonify(supply_list), 200

# Supply Orders
@routes.route('/api/supply_orders', methods=['GET'])
def get_supply_orders():
    supply_orders = SupplyOrder.query.all()
    supply_order_list = [
        {
            'id': supply_order.ID,
            'supply_id': supply_order.SupplyID,
            'order_date': supply_order.Order_date.strftime('%Y-%m-%d'),
            'quantity': supply_order.Quantity
        }
        for supply_order in supply_orders
    ]
    return jsonify(supply_order_list), 200

# Manufacturers
@routes.route('/api/manufacturers', methods=['GET'])
def get_manufacturers():
    manufacturers = Manufacturer.query.all()
    manufacturer_list = [
        {
            'id': manufacturer.ID,
            'name': manufacturer.Companyname,
            'contact_info': manufacturer.Contactinfo
        }
        for manufacturer in manufacturers
    ]
    return jsonify(manufacturer_list), 200

# Categories
@routes.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [
        {
            'id': category.ID,
            'name': category.Categoryname
        }
        for category in categories
    ]
    return jsonify(category_list), 200

# Admins
@routes.route('/api/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    admin_list = [
        {
            'id': admin.ID,
            'username': admin.Username,
            'email': admin.Email
        }
        for admin in admins
    ]
    return jsonify(admin_list), 200
