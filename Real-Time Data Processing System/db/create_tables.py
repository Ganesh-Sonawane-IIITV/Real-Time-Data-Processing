# db/create_tables.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import DB_URL
import psycopg2

def create_tables():
    # Connect to PostgreSQL
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # SQL queries to create the necessary tables
    create_weather_data_table = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city TEXT NOT NULL,
        temperature FLOAT NOT NULL,
        feels_like FLOAT NOT NULL,
        weather_condition TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL
    );
    """

    create_daily_weather_summary_table = """
    CREATE TABLE IF NOT EXISTS daily_weather_summary (
        id SERIAL PRIMARY KEY,
        city TEXT NOT NULL,
        avg_temp FLOAT NOT NULL,
        max_temp FLOAT NOT NULL,
        min_temp FLOAT NOT NULL,
        dominant_weather_condition TEXT NOT NULL,
        date DATE NOT NULL
    );
    """

    # Execute SQL queries
    cur.execute(create_weather_data_table)
    cur.execute(create_daily_weather_summary_table)

    # Commit and close connection
    conn.commit()
    cur.close()
    conn.close()

    print("Tables created successfully")

# Call the function to create tables
if __name__ == "__main__":
    create_tables()
