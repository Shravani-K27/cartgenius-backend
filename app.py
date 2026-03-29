
import os

from flask import Flask, jsonify
from flask_cors import CORS
from model import recommend_similar_products

app = Flask(__name__)
CORS(app)  # 🔥 IMPORTANT

@app.route('/')
def home():
    return "CartGenius API is running 🚀"

@app.route('/recommend_item/<product>')
def recommend_item(product):
    return jsonify(recommend_similar_products(product))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    