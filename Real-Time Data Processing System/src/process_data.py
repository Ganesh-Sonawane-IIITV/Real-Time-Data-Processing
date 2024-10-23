# src/process_data.py

import psycopg2
from config.config import DB_URL
from src.fetch_weather import fetch_all_cities
from datetime import datetime, timedelta
import logging
def store_weather_data(weather_data):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    insert_query = """
    INSERT INTO weather_data (city, temperature, feels_like, weather_condition, timestamp)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    for data in weather_data:
        cur.execute(insert_query, (
            data['city'], 
            data['temperature'], 
            data['feels_like'], 
            data['weather_condition'], 
            data['timestamp']
        ))
    
    conn.commit()
    cur.close()
    conn.close()

def aggregate_daily_summary():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Get yesterday's date
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    
    # Calculate aggregates for each city
    cur.execute("""
    SELECT city, 
           AVG(temperature) AS avg_temp, 
           MAX(temperature) AS max_temp, 
           MIN(temperature) AS min_temp
    FROM weather_data
    WHERE DATE(timestamp) = %s
    GROUP BY city;
    """, (yesterday,))

    summaries = cur.fetchall()

    # Insert summaries into daily_weather_summary table
    insert_query = """
    INSERT INTO daily_weather_summary (city, avg_temp, max_temp, min_temp, date)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    for summary in summaries:
        cur.execute(insert_query, (
            summary[0],  # city
            summary[1],  # avg_temp
            summary[2],  # max_temp
            summary[3],  # min_temp
            summary[4],  # dominant_weather_condition
            yesterday     # date
        ))
    
    conn.commit()
    cur.close()
    conn.close()

# def aggregate_daily_summary():
#     conn = psycopg2.connect(DB_URL)
#     cur = conn.cursor()

#     now = datetime.utcnow()  # Current time
    
#     try:
#         # Calculate aggregates for each city for all data in the weather_data table
#         cur.execute("""
#         SELECT city, 
#                AVG(temperature) AS avg_temp, 
#                MAX(temperature) AS max_temp, 
#                MIN(temperature) AS min_temp,
#                MODE() WITHIN GROUP (ORDER BY weather_condition) AS dominant_weather_condition
#         FROM weather_data
#         GROUP BY city;
#         """)

#         summaries = cur.fetchall()

#         # Insert summaries into daily_weather_summary table
#         insert_query = """
#         INSERT INTO daily_weather_summary (city, avg_temp, max_temp, min_temp, dominant_weather_condition, date)
#         VALUES (%s, %s, %s, %s, %s, %s)
#         ON CONFLICT (city, date) 
#         DO UPDATE SET 
#             avg_temp = EXCLUDED.avg_temp, 
#             max_temp = EXCLUDED.max_temp, 
#             min_temp = EXCLUDED.min_temp, 
#             dominant_weather_condition = EXCLUDED.dominant_weather_condition;
#         """

#         # Loop through the aggregated summaries and store them
#         for summary in summaries:
#             cur.execute(insert_query, (
#                 summary[0],  # city
#                 summary[1],  # avg_temp
#                 summary[2],  # max_temp
#                 summary[3],  # min_temp
#                 summary[4],  # dominant_weather_condition
#                 now.date()   # date
#             ))
        
#         conn.commit()
#         logging.info(f"Daily summary updated for {len(summaries)} cities at {now}")
    
#     except Exception as e:
#         logging.error(f"Error during aggregation: {e}")
    
#     finally:
#         cur.close()
#         conn.close()

# def process_weather_data():
#     weather_data = fetch_all_cities()
#     store_weather_data(weather_data)
#     print(f"Weather data processed and stored at {datetime.utcnow()}")
    
#     # Optionally, you can call aggregate_daily_summary() here based on certain conditions
#     # For example, if it's midnight UTC, perform the aggregation
#     now = datetime.utcnow()
#     if now.hour == 0 and now.minute == 0:
#         aggregate_daily_summary()
#         print(f"Daily summary aggregated at {now}")

def check_alerts():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Example: Alert if temperature > 35°C for two consecutive updates
    cur.execute("""
    SELECT city, COUNT(*) 
    FROM weather_data
    WHERE temperature > 30
      AND timestamp > NOW() - INTERVAL '10 minutes' -- Assuming FETCH_INTERVAL is 5 minutes
    GROUP BY city
    HAVING COUNT(*) >= 2;
    """)

    alerts = cur.fetchall()

    for alert in alerts:
        city, count = alert
        print(f"ALERT: {city} has exceeded 30°C for {count} consecutive updates.")

    cur.close()
    conn.close()

def process_weather_data():
    weather_data = fetch_all_cities()
    store_weather_data(weather_data)
    print(f"Weather data processed and stored at {datetime.utcnow()}")
    
    # Check for alerts after storing new data
    check_alerts()
    
    # Optionally, aggregate daily summaries
    now = datetime.utcnow()
    if now.hour == 0 and now.minute == 0:
        aggregate_daily_summary()
        print(f"Daily summary aggregated at {now}")
# def process_weather_data():
#     # Fetch and store new weather data
#     weather_data = fetch_all_cities()  # Fetch weather data for all cities
#     store_weather_data(weather_data)   # Store the fetched data
#     print(f"Weather data processed and stored at {datetime.utcnow()}")

#     # Check for alerts after storing new data
#     check_alerts()

#     # Aggregate daily summaries every 5 minutes
#     aggregate_daily_summary()  # Call the aggregation function after every processing 

def get_current_alerts():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Example: Alert if temperature > 35°C for two consecutive updates
    cur.execute("""
        SELECT city, COUNT(*)
        FROM weather_data
        WHERE temperature > 30
          AND timestamp > NOW() - INTERVAL '10 minutes'
        GROUP BY city
        HAVING COUNT(*) >= 2;
    """)
    alerts = cur.fetchall()
    
    cur.close()
    conn.close()
    return alerts
# if __name__ == "__main__":
#     process_weather_data()
