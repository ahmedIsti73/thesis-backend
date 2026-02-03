import os
import json
from web3 import Web3
from pathlib import Path

# 1. CONNECT TO BLOCKCHAIN
# Logic: If 'ALCHEMY_URL' exists (Cloud), use it. Otherwise, use Localhost.
alchemy_url = os.getenv("ALCHEMY_URL", "http://127.0.0.1:8545")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# 2. LOAD THE CONTRACT (The "Bridge")
# This finds the file created by your deploy.js script
base_path = Path(__file__).parent
json_path = base_path / "contract_data.json"

contract = None

if json_path.exists():
    with open(json_path, "r") as f:
        data = json.load(f)
        address = data["address"]
        abi = data["abi"]
        
        # Create the Contract Object
        if address and abi:
            contract = w3.eth.contract(address=address, abi=abi)
            print(f"Python Connected to Contract at: {address}")
else:
    print("⚠️ Warning: contract_data.json not found. Run deploy.js first!")