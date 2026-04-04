import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity
import os

# 🔹 DB Connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

# 🔹 Main Recommendation Function
def recommend_similar_products(product_name, top_n=5):
    try:
        conn = get_connection()

        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, conn)

        # Data Cleaning
        df = df.dropna()
        df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
        df['CustomerID'] = df['CustomerID'].astype(int)

        # User-Product Matrix
        user_product_matrix = df.pivot_table(
            index='CustomerID',
            columns='Description',
            values='Quantity',
            fill_value=0
        )

        product_matrix = user_product_matrix.T

        similarity = cosine_similarity(product_matrix)

        similarity_df = pd.DataFrame(
            similarity,
            index=product_matrix.index,
            columns=product_matrix.index
        )

        # Recommendation Logic
        if product_name not in similarity_df.index:
            return ["Product not found"]

        similar_items = similarity_df[product_name] \
            .sort_values(ascending=False) \
            .iloc[1:top_n+1]

        return list(similar_items.index)

    except Exception as e:
        return [f"Error: {str(e)}"]