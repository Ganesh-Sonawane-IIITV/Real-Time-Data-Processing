# Real-Time Data Processing System

## Overview

The Real-Time Data Processing System is designed to monitor and analyze weather data in real time. It aggregates weather information, generates daily summaries, and triggers alerts based on user-defined thresholds. This project serves as a powerful tool for understanding weather patterns and receiving timely notifications of significant changes in weather conditions.

## Project Structure
```bash
Real-Time Data Processing System/
│
├── config/
│   └── config.py                  # Configuration file for database connection
├── db/
│   └── create_tables.py           # Script for creating the PostgreSQL tables
├── src/
│   ├── fetch_weather.py           # Fetches current weather data from API
│   ├── process_data.py            # Processes weather data for summaries and alerts
│   └── visualize.py                # Handles data visualization for trends and summaries
├── static/
│   ├── css/
│   │   └── style.css              # CSS file for styling the UI
│   └── js/
│       └── script.js              # JavaScript file for client-side logic
├── templates/
│   ├── index.html                 # Main UI template for displaying weather data
│   ├── daily_weather_summary.html  # Template for displaying daily weather summaries
│   └── weather_alerts.html        # Template for displaying weather alerts
├── app.py                         # Main application entry point for Flask
├── main.py                        # Entry point for running the weather monitoring logic
└── requirements.txt               # List of dependencies for the project
```


## Features

### 1. Daily Weather Summary
- Roll up the weather data for each day.
- Calculate daily aggregates for:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition (determined by the most frequently reported condition for the day).
- Store the daily summaries in a database for further analysis.

### 2. Alerting Thresholds
- Define user-configurable thresholds for temperature or specific weather conditions (e.g., alert if temperature exceeds 35 degrees Celsius for two consecutive updates).
- Continuously track the latest weather data and compare it with the thresholds.
- Trigger alerts for current weather conditions if a threshold is breached. Alerts can be displayed in the console or sent via an email notification system.

### 3. Visualizations
- Implement visualizations to display:
  - Daily weather summaries
  - Historical trends
  - Triggered alerts

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Real-Time Data Processing System
   ```
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database:**
   Run ```create_tables.py``` to set up the necessary database tables.
4. **Run the application:**
   ```bash
   python main.py
   ```
5. **Access the application:**
   Open your web browser and navigate to ```http://127.0.0.1:5000/```

## Screenshots

### Current Weather Data
![Current Weather Data](https://raw.githubusercontent.com/Ganesh-Sonawane-IIITV/Real-Time-Data-Processing/refs/heads/main/Real-Time%20Data%20Processing%20System/Images/current_weather_data.png)
*Displays the most recent weather data fetched from the API.*

### Daily Weather Summary
![Daily Weather Summary](https://raw.githubusercontent.com/Ganesh-Sonawane-IIITV/Real-Time-Data-Processing/refs/heads/main/Real-Time%20Data%20Processing%20System/Images/daily_weather_summary%20and%20weather%20alerts.png)  
*Shows the daily weather summary, including average, maximum, and minimum temperatures.*
*Illustrates alerts triggered based on predefined temperature thresholds.*

### Temperature Trends
![Temperature Trends](https://raw.githubusercontent.com/Ganesh-Sonawane-IIITV/Real-Time-Data-Processing/refs/heads/main/Real-Time%20Data%20Processing%20System/Images/temperature%20trends.png)  
*Visual representation of temperature trends over time, highlighting changes in weather patterns.*
