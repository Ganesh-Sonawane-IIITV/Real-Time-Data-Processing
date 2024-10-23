# # app.py

# from flask import Flask, render_template
# import psycopg2
# from config.config import DB_URL, FETCH_INTERVAL
# from src.process_data import process_weather_data, get_current_alerts
# import threading
# import time

# app = Flask(__name__)

# # Connect to the PostgreSQL database
# def get_db_connection():
#     conn = psycopg2.connect(DB_URL)
#     return conn

# @app.route('/api/daily_summary')
# def get_daily_summary():
#     conn = get_db_connection()
#     cur = conn.cursor()
    
#     # Fetch daily summaries from the database
#     cur.execute("""
#         SELECT city, avg_temp
#         FROM daily_weather_summary
#         ORDER BY date DESC
#         LIMIT 6;
#     """)
#     daily_summary = cur.fetchall()
    
#     cur.close()
#     conn.close()

#     # Convert the data to a format suitable for JSON response
#     summary_data = {
#         "cities": [row[0] for row in daily_summary],
#         "avg_temps": [row[1] for row in daily_summary]
#     }
    
#     return jsonify(summary_data)






# # Route for the main UI
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cur = conn.cursor()
    
#     # Fetch the latest weather data from the database
#     cur.execute("""
#     SELECT DISTINCT city, temperature, feels_like, weather_condition, timestamp
#     FROM weather_data
#     ORDER BY timestamp DESC
#     LIMIT 6;
#     """)
#     weather_data = cur.fetchall()

#     # Fetch daily summaries (for visualization)
#     cur.execute("""
#     SELECT city, avg_temp, max_temp, min_temp, dominant_weather_condition, date
#     FROM daily_weather_summary
#     ORDER BY date DESC;
#     """)
#     daily_summary = cur.fetchall()


#     # Fetch current alerts
#     # cur.execute("""
#     # SELECT city, COUNT(*) 
#     # FROM weather_data
#     # WHERE temperature > 35
#     #   AND timestamp > NOW() - INTERVAL '10 minutes' 
#     # GROUP BY city
#     # HAVING COUNT(*) >= 2;
#     # """)
#     # alerts = cur.fetchall()
#     alerts = get_current_alerts()

#     cur.close()
#     conn.close()

#     return render_template('index.html', weather_data=weather_data, daily_summary=daily_summary, alerts=alerts)

# def run_data_processing():
#     while True:
#         try:
#             process_weather_data()
#         except Exception as e:
#             print(f"Error during data processing: {e}")
#         time.sleep(FETCH_INTERVAL)

# if __name__ == '__main__':
#     # Start the data processing in a separate thread
#     data_thread = threading.Thread(target=run_data_processing, daemon=True)
#     data_thread.start()
    
#     # Run the Flask app
#     app.run(debug=True)
from flask import Flask, render_template, jsonify  # Import jsonify
import psycopg2
from config.config import DB_URL, FETCH_INTERVAL
from src.process_data import process_weather_data, get_current_alerts
import threading
import time

app = Flask(__name__)

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

@app.route('/api/daily_summary')
def get_daily_summary():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch daily summaries from the database
    cur.execute("""SELECT city, avg_temp FROM daily_weather_summary ORDER BY date DESC LIMIT 6;""")
    daily_summary = cur.fetchall()
    
    cur.close()
    conn.close()

    # Convert the data to a format suitable for JSON response
    summary_data = {
        "cities": [row[0] for row in daily_summary],
        "avg_temps": [row[1] for row in daily_summary]
    }
    
    return jsonify(summary_data)

@app.route('/api/weather_data')
def get_weather_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch the latest weather data for distinct cities
    cur.execute("""
        SELECT  DISTINCT city, temperature
        FROM weather_data wd1
        WHERE timestamp = (
            SELECT MAX(timestamp)
            FROM weather_data wd2
            WHERE wd1.city = wd2.city
        )
        ORDER BY city  LIMIT 6;
    """)
    weather_data = cur.fetchall()
    
    cur.close()
    conn.close()

    # Convert the data to a format suitable for JSON response
    weather_data_json = {
        "cities": [row[0] for row in weather_data],
        "temperatures": [row[1] for row in weather_data]
    }
    
    return jsonify(weather_data_json)




# Route for the main UI
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch the latest weather data from the database
    cur.execute("""SELECT DISTINCT city, temperature, feels_like, weather_condition, timestamp FROM weather_data ORDER BY timestamp DESC LIMIT 6;""")
    weather_data = cur.fetchall()

    # Fetch daily summaries (for visualization)
    cur.execute("""SELECT city, avg_temp, max_temp, min_temp, date FROM daily_weather_summary ORDER BY date DESC;""")
    daily_summary = cur.fetchall()

    # Fetch current alerts
    alerts = get_current_alerts()

    cur.close()
    conn.close()

    return render_template('index.html', weather_data=weather_data, daily_summary=daily_summary, alerts=alerts)

def run_data_processing():
    while True:
        try:
            process_weather_data()
        except Exception as e:
            print(f"Error during data processing: {e}")
        time.sleep(FETCH_INTERVAL)

if __name__ == '__main__':
    # Start the data processing in a separate thread
    data_thread = threading.Thread(target=run_data_processing, daemon=True)
    data_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
