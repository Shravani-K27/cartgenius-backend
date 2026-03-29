import pandas as pd
import mysql.connector

print("🚀 Script started...")

# Load CSV
df = pd.read_csv("data.csv", encoding='latin1')
print("✅ CSV Loaded. Rows:", len(df))

# Fix datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Drop bad rows
df = df.dropna()
print("✅ Cleaned Data. Rows:", len(df))

# Connect MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  
    database="cartgenius"
)

cursor = conn.cursor()
print("✅ Connected to MySQL")

count = 0

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO transactions
        (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['InvoiceNo'],
        row['StockCode'],
        row['Description'],
        int(row['Quantity']),
        row['InvoiceDate'].strftime('%Y-%m-%d %H:%M:%S'),
        float(row['UnitPrice']),
        int(row['CustomerID']),
        row['Country']
    ))
    count += 1

conn.commit()

print("🎉 DONE! Rows inserted:", count)