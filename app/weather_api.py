import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather(self, location):
        """Get current weather for a location"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def get_forecast(self, location):
        """Get 5-day forecast for a location"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecast = []
            for item in data['list']:
                forecast.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'temperature': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            return forecast
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
