import pytest
from app.weather_api import WeatherAPI
from unittest.mock import patch, MagicMock

@pytest.fixture
def weather_api():
    return WeatherAPI()

def test_get_weather_success(weather_api):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'main': {
            'temp': 20,
            'feels_like': 22,
            'humidity': 65
        },
        'weather': [{
            'description': 'clear sky',
            'icon': '01d'
        }],
        'wind': {
            'speed': 5
        }
    }
    
    with patch('requests.get', return_value=mock_response):
        result = weather_api.get_weather('London')
        
        assert result['temperature'] == 20
        assert result['feels_like'] == 22
        assert result['humidity'] == 65
        assert result['description'] == 'clear sky'
        assert result['icon'] == '01d'
        assert result['wind_speed'] == 5

def test_get_weather_error(weather_api):
    with patch('requests.get', side_effect=Exception('API Error')):
        result = weather_api.get_weather('Invalid Location')
        assert 'error' in result
