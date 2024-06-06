from flask import Flask, jsonify, request
import requests
import datetime
import sqlite3
import threading
import schedule
import time

# Initialize Flask app
app = Flask(__name__)

# Constants for the cryptocurrency API and database
API_URL = "https://api.coingecko.com/api/v3/simple/price"
CURRENCIES = ["eur", "czk"]
DATABASE = 'btc_prices.db'
AUTH_TOKEN = '37c9a1b2cf9b1d3a9d87e6be6b37d3a4'  # Replace with your actual secure token

# Fetch current BTC price in EUR and CZK
def fetch_current_price():
    response = requests.get(API_URL, params={"ids": "bitcoin", "vs_currencies": ",".join(CURRENCIES)})
    return response.json()

# Get a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the SQLite database
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS prices (
                      time TIMESTAMP PRIMARY KEY,
                      eur REAL,
                      czk REAL)''')
    conn.commit()
    conn.close()

# Store BTC price in the database
def store_price():
    prices = fetch_current_price()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (time, eur, czk) VALUES (?, ?, ?)",
                   (datetime.datetime.now(datetime.timezone.utc), prices['bitcoin']['eur'], prices['bitcoin']['czk']))
    conn.commit()
    conn.close()

# Scheduler job to store BTC price every 5 minutes
def job():
    store_price()

schedule.every(5).minutes.do(job)

# Run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Endpoint to fetch current BTC price
@app.route('/current-price', methods=['GET'])
def current_price():
    print("Received request for current price")
    if not authenticate_request(request):
        print("Unauthorized request")
        return jsonify({"error": "Unauthorized"}), 401
    prices = fetch_current_price()
    server_time = datetime.datetime.now(datetime.timezone.utc)
    response = {
        "btc_prices": prices,
        "currency": CURRENCIES,
        "client_request_time": datetime.datetime.now(datetime.timezone.utc),
        "server_data_time": server_time
    }
    print("Response: ", response)
    return jsonify(response)

# Calculate daily and monthly averages
def calculate_averages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prices WHERE time >= datetime('now', '-1 day')")
    daily_prices = cursor.fetchall()
    cursor.execute("SELECT * FROM prices WHERE time >= datetime('now', '-1 month')")
    monthly_prices = cursor.fetchall()
    conn.close()

    daily_avg = sum([row['eur'] for row in daily_prices]) / len(daily_prices), sum([row['czk'] for row in daily_prices]) / len(daily_prices)
    monthly_avg = sum([row['eur'] for row in monthly_prices]) / len(monthly_prices), sum([row['czk'] for row in monthly_prices]) / len(monthly_prices)

    return daily_avg, monthly_avg

# Endpoint to fetch daily and monthly averages
@app.route('/averages', methods=['GET'])
def averages():
    print("Received request for averages")
    if not authenticate_request(request):
        print("Unauthorized request")
        return jsonify({"error": "Unauthorized"}), 401
    daily_avg, monthly_avg = calculate_averages()
    response = {
        "daily_average": {"eur": daily_avg[0], "czk": daily_avg[1]},
        "monthly_average": {"eur": monthly_avg[0], "czk": monthly_avg[1]},
        "client_request_time": datetime.datetime.now(datetime.timezone.utc)
    }
    print("Response: ", response)
    return jsonify(response)

# Authentication function
def authenticate_request(request):
    token = request.headers.get('Authorization')
    print("Authorization token: ", token)
    return token == AUTH_TOKEN

# Main function to initialize database, start scheduler and run Flask app
if __name__ == '__main__':
    initialize_db()
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app.run(host='0.0.0.0', port=5000)
