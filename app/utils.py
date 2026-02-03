import jwt
import datetime
from flask import current_app

def generate_token(public_address):
    """
    Generates a JWT (Session Ticket) for the user.
    valid for 24 hours.
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), # Expires in 1 day
            'iat': datetime.datetime.utcnow(), # Issued at
            'sub': public_address # Subject (The User's Wallet Address)
        }
        # We use a secret key to sign the ticket so no one can fake it
        return jwt.encode(
            payload, 
            'THESIS_SUPER_SECRET_KEY', # In production, this goes in .env
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)

def decode_token(token):
    """
    Reads the ticket to see who the user is.
    """
    try:
        payload = jwt.decode(token, 'THESIS_SUPER_SECRET_KEY', algorithms=['HS256'])
        return payload['sub'] # Returns the wallet address
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token."