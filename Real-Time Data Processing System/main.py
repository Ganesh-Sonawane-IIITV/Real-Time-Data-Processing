# main.py

import time
from src.process_data import process_weather_data
from config.config import FETCH_INTERVAL

if __name__ == "__main__":
    while True:
        process_weather_data()
        time.sleep(FETCH_INTERVAL)
