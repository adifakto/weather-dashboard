import unittest
from unittest.mock import patch, MagicMock
import requests
from model import WeatherModel


class TestWeatherModel(unittest.TestCase):

    def test_singleton(self):
        api_key = "dummy_api_key"
        model1 = WeatherModel(api_key)
        model2 = WeatherModel(api_key)
        self.assertIs(model1, model2)
        self.assertEqual(model1.api_key, "dummy_api_key")
        self.assertEqual(model2.api_key, "dummy_api_key")

    @patch('requests.get')
    def test_fetch_weather_success(self, mock_get):
        api_key = "dummy_api_key"
        model = WeatherModel(api_key)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {
                "temp": 22,
                "feels_like": 21,
                "temp_min": 18,
                "temp_max": 26,
                "pressure": 1013,
                "humidity": 60
            },
            "weather": [{"main": "Sunny"}],
            "clouds": {"all": 10},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"sunrise": 1632456933, "sunset": 1632500853},
            "timezone": 3600
        }
        
        mock_get.return_value = mock_response
        
        city_name = "TestCity"
        data = model.fetch_weather(city_name)
        
        self.assertEqual(data["temperature"], 22)
        self.assertEqual(data["weather_condition"], "Sunny")
        self.assertEqual(data["feels_like"], 21)
        self.assertEqual(data["min_tempreture"], 18)
        self.assertEqual(data["max_tempreture"], 26)
        self.assertEqual(data["pressure"], 1013)
        self.assertEqual(data["humidity"], 60)
        self.assertEqual(data["clouds"], 10)
        self.assertEqual(data["visibility"], 10000)
        self.assertEqual(data["wind_speed"], 5)
        self.assertEqual(data["sunrise"], 1632456933)
        self.assertEqual(data["sunset"], 1632500853)
        self.assertEqual(data["timezone"], 3600)

    @patch('requests.get')
    def test_fetch_weather_error_response(self, mock_get):
        api_key = "dummy_api_key"
        model = WeatherModel(api_key)
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        city_name = "InvalidCity"
        data = model.fetch_weather(city_name)
        
        self.assertIsNone(data)

    @patch('requests.get')
    def test_fetch_weather_request_exception(self, mock_get):
        api_key = "dummy_api_key"
        model = WeatherModel(api_key)
        
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        city_name = "TestCity"
        data = model.fetch_weather(city_name)
        
        self.assertIsNone(data)

    def test_api_key_initialization(self):
        api_key = "dummy_api_key"
        model = WeatherModel(api_key)
        
        self.assertEqual(model.api_key, "dummy_api_key")

if __name__ == "__main__":
    unittest.main()
