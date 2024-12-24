import streamlit as st
import requests
from datetime import datetime

# Function to get AQI data
def get_aqi(lon, lat, api_key):
    """
    Fetches the real-time AQI for a given city using OpenWeatherMap API.

    Args:
        lon (float): Longitude of the location.
        lat (float): Latitude of the location.
        api_key (str): The API key for OpenWeatherMap.

    Returns:
        dict or None: Returns AQI data if successful, otherwise None.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    # Make a request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return None