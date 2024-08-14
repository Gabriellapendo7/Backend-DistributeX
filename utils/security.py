from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

def generate_reset_token(user_id, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_reset_token(token, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    try:
        data = s.loads(token)
    except:
        return None
    return data.get('user_id')