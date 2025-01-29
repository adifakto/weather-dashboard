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
                    "weather_condition": data["weather"][0]["main"],
                    "feels_like": data["main"]["feels_like"],
                    "min_tempreture": data["main"]["temp_min"],
                    "max_tempreture": data["main"]["temp_max"],
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                    "sea_level": data["main"]["sea_level"],
                    "visability": data["visibility"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_degree": data["wind"]["deg"],
                    "sunrise": data["sys"]["sunrise"],
                    "sunset": data["sys"]["sunset"]
                }
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None