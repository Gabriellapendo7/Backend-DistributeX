from flask_mail import Message
from flask import current_app
from . import mail

def send_reset_email(user, token):
    msg = Message('Password Reset Request', sender='your-email@example.com', recipients=[user.Email])
    msg.body = f'''
    To reset your password, visit the following link:
    {current_app.config['APP_URL']}/reset_password/{token}
    '''
    mail.send(msg)