# src/fetch_weather.py

import requests
from config.config import API_KEY, CITIES
from datetime import datetime

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main_data = data["main"]
        weather_condition = data["weather"][0]["main"]
        temp = kelvin_to_celsius(main_data["temp"])
        feels_like = kelvin_to_celsius(main_data["feels_like"])
        timestamp = datetime.utcfromtimestamp(data["dt"])
        
        return {
            "city": city,
            "temperature": temp,
            "feels_like": feels_like,
            "weather_condition": weather_condition,
            "timestamp": timestamp
        }
    else:
        print(f"Failed to fetch weather data for {city}")
        return None

def fetch_all_cities():
    weather_data = []
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            weather_data.append(data)
    return weather_data
