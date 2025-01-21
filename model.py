import requests

class WeatherModel:
    _instance = None

    def __new__(cls, api_key=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.api_key = api_key
        return cls._instance

    def fetch_weather(self, city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temperature": data["main"]["temp"],
                    "weather_condition": data["weather"][0]["description"]
                }
            else:
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None    
