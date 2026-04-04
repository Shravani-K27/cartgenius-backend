import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from model import recommend_similar_products

app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return "CartGenius API is running 🚀"

# Route 1: URL parameter
@app.route('/recommend_item/<product>')
def recommend_item(product):
    return jsonify(recommend_similar_products(product))

# Route 2: Query parameter
@app.route('/recommend')
def recommend():
    product = request.args.get("product")
    return jsonify(recommend_similar_products(product))

# IMPORTANT: Always keep this at the END
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))