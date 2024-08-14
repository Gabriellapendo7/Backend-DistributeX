from flask import Blueprint, make_response, request, current_app
from flask_restful import Api, Resource
from models import Manufacturer, db
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from flask_bcrypt import Bcrypt
import logging

bcrypt = Bcrypt()

manufacturer_pass_recovery_bp = Blueprint('manufacturer_pass_recovery_bp', __name__, url_prefix='/manufacturer')
manufacturer_pass_recovery_api = Api(manufacturer_pass_recovery_bp)

logging.basicConfig(level=logging.DEBUG)

class ManufacturerPasswordRecovery(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')

            manufacturer = Manufacturer.query.filter_by(Email=email).first()

            if manufacturer:
                recovery_token = create_recovery_token(manufacturer)

                subject = 'Password Recovery'
                body = f"To reset your password, click the link: http://localhost:3000/manufacturer-reset-password/{recovery_token}"

                send_email(email, subject, body)
                return make_response({'message': 'Recovery email sent successfully'}, 200)
            else:
                return make_response({'message': 'Email not found'}, 404)
        except Exception as e:
            logging.error(f"Error in ManufacturerPasswordRecovery: {e}")
            return make_response({'message': 'An error occurred', 'error': str(e)}, 500)

def create_recovery_token(manufacturer, expires_in=3600):
    s = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt='password-recovery-salt'
    )
    return s.dumps(manufacturer.Email, salt='password-recovery-salt')

manufacturer_pass_recovery_api.add_resource(ManufacturerPasswordRecovery, '/recovery_password', strict_slashes=False)

class ManufacturerResetPassword(Resource):
    def post(self):
        try:
            data = request.get_json()
            recovery_token = data.get('recovery_token')
            new_password = data.get('new_password')

            if not recovery_token or not new_password:
                return make_response({'message': 'Missing recovery token or new password'}, 400)

            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='password-recovery-salt')

            try:
                email = s.loads(recovery_token, salt='password-recovery-salt')
            except Exception as e:
                logging.error(f"Token validation error: {e}")
                return make_response({'message': 'Invalid or expired recovery token'}, 400)

            manufacturer = Manufacturer.query.filter_by(Email=email).first()

            if manufacturer:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

                manufacturer.Password = hashed_password
                db.session.commit()

                return make_response({'message': 'Password reset successfully'}, 200)
            else:
                return make_response({'message': 'Manufacturer not found'}, 404)
        except Exception as e:
            logging.error(f"Error in ManufacturerResetPassword: {e}")
            return make_response({'message': 'An error occurred', 'error': str(e)}, 500)
        
manufacturer_pass_recovery_api.add_resource(ManufacturerResetPassword, '/reset_password', strict_slashes=False)

def send_email(to_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = current_app.config['MAIL_USERNAME']
    password = current_app.config['MAIL_PASSWORD']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(from_email, password)  
            server.sendmail(from_email, [to_email], msg.as_string())
    except Exception as e:
        logging.error(f"Email sending error: {e}")
        raise e
