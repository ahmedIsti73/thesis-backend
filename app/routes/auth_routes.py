import random
from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from app.utils import generate_token
from eth_account.messages import encode_defunct

# Import the 'w3' that knows about Alchemy/Cloud
from app.blockchain.client import w3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/nonce', methods=['GET'])
def get_nonce():
    """
    Step 1: Frontend asks for a random number (Nonce).
    We generate it, save it to the DB, and send it back.
    """
    public_address = request.args.get('publicAddress')
    
    if not public_address:
        return jsonify({"error": "Missing publicAddress"}), 400

    # Check if user exists, if not, create them
    user = User.query.filter_by(public_address=public_address).first()
    
    # Generate a random big number
    nonce = random.randint(100000, 999999)

    if not user:
        # Create new user (Hybrid Model: Address on DB)
        user = User(public_address=public_address, nonce=nonce)
        db.session.add(user)
    else:
        # Update existing user's nonce
        user.nonce = nonce
    
    db.session.commit()
    
    return jsonify({"nonce": nonce})

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Step 2: Frontend sends the signature.
    We verify it matches the Nonce we saved.
    """
    data = request.get_json()
    public_address = data.get('publicAddress')
    signature = data.get('signature')

    if not public_address or not signature:
        return jsonify({"error": "Missing data"}), 400

    # 1. Get the user from DB to find the expected Nonce
    user = User.query.filter_by(public_address=public_address).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 2. Re-create the message that was signed
    # The message must be: "I am signing my one-time nonce: 123456"
    msg = f"I am signing my one-time nonce: {user.nonce}"
    
    # 3. Recover the address from the signature (Cryptography Magic)
    try:
        message_hash = encode_defunct(text=msg)
        recovered_address = w3.eth.account.recover_message(message_hash, signature=signature)
    except Exception as e:
        return jsonify({"error": f"Recovery failed: {str(e)}"}), 400

    # 4. Compare addresses
    if recovered_address.lower() == public_address.lower():
        # SUCCESS! Issue the JWT Ticket
        token = generate_token(public_address)
        return jsonify({
            "token": token,
            "message": "Login Successful!"
        })
    else:
        return jsonify({"error": "Signature verification failed"}), 401