# Created by ChatGPT

import requests
from datetime import datetime

def get_weather_data():
    # Latitude and longitude for Mansfield, Texas
    lat, lon = 32.5632, -97.1417
    
    # API endpoint
    url = f"https://api.weather.gov/points/{lat},{lon}"
    
    # Get the forecast URL
    response = requests.get(url)
    data = response.json()
    forecast_url = data['properties']['forecast']
    
    # Get the forecast data
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    return forecast_data['properties']['periods']

def generate_weather_summary(weather_data):
    today = weather_data[0]  # Today's forecast
    tonight = weather_data[1]  # Tonight's forecast (for low temperature)

    high_temp = today['temperature']
    low_temp = tonight['temperature']
    temp_unit = today['temperatureUnit']
    wind_speed = today['windSpeed']
    wind_direction = today['windDirection']
    short_forecast = today['shortForecast']
    detailed_forecast = today['detailedForecast']

    # Check for rain
    rain_chance = "No mention of rain."
    if 'rain' in detailed_forecast.lower() or 'precipitation' in detailed_forecast.lower():
        rain_chance = "There is a chance of rain today."

    return high_temp, low_temp, temp_unit, wind_speed, wind_direction, short_forecast, detailed_forecast, rain_chance

def main():
    weather_data = get_weather_data()
    summary = generate_weather_summary(weather_data)
    print(summary)

if __name__ == "__main__":
    main()