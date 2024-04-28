from flask import Flask, render_template, request, jsonify
from pi_network import PiNetwork  # Assuming your Python code is in pi_network.py

app = Flask(__name__)
pi_network = PiNetwork()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_balance', methods=['GET'])
def get_balance():
    balance = pi_network.get_balance()
    return jsonify({'balance': balance})

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.json
    amount = data.get('amount')
    memo = data.get('memo')

    # Assuming you have a method to create a payment in your PiNetwork class
    payment_id = pi_network.create_payment(amount, memo)
    
    return jsonify({'payment_id': payment_id})

if __name__ == '__main__':
    # Initialize PiNetwork object with API key, private key, and network
    pi_network.initialize(api_key='your_api_key', wallet_private_key='your_private_key', network='Pi Network')
    app.run(debug=True)
