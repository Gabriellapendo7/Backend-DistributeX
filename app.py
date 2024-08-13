from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config, db, ma, migrate, bcrypt, mail
from routes.manufacturerAuth import manufacturer_auth_bp 
from routes.supply import supply_bp 
from routes.supply_order import supply_order_bp 
from routes.forgetPass import manufacturer_pass_recovery_bp

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})  
    app.config.from_object(Config)

    # Mail server configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'timon.dando@student.moringaschool.com'
    app.config['MAIL_PASSWORD'] = 'ptseaiccqtylremr'
    app.config['MAIL_DEFAULT_SENDER'] = 'dandobrandon0@gmail.com'

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)

    api = Api(app)

    app.register_blueprint(manufacturer_auth_bp)  
    app.register_blueprint(supply_bp)
    app.register_blueprint(supply_order_bp, url_prefix='/api')
    app.register_blueprint(manufacturer_pass_recovery_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
