
from threading import Thread, Lock

class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_refreshing = False
        self.lock = Lock()  # Add a lock for thread safety

        # Bind buttons to methods
        self.view.add_city_button.config(command=self.add_city_if_not_refreshing)
        self.view.refresh_button.config(command=self.update_weather)


    def add_city_if_not_refreshing(self):
        """Adds a city only if not currently refreshing."""
        if not self.is_refreshing:
            self.view.add_city()

    def update_weather(self):
        """Updates weather data for all cities in a background thread."""
        if self.is_refreshing:
            return  # Prevent multiple refreshes

        self.is_refreshing = True
        self.view.disable_all_buttons()  # Disable buttons immediately

        # Start a background thread to fetch weather data
        Thread(target=self._fetch_weather_data, daemon=True).start()

    def _fetch_weather_data(self):
        """Fetches weather data for all cities in the background."""
        try:
            for city_index, city_entry in enumerate(self.view.city_entries):
                city_name = city_entry.get()
                try:
                    data = self.model.fetch_weather(city_name)
                    if data:
                        self._update_ui(
                            city_index,
                            f"Temperature: {data['temperature']}°C",
                            f"Condition: {data['weather_condition']}",
                            f"{data['min_tempreture']}°C/{data['max_tempreture']}°C",
                            f"Feels Like: {data['feels_like']}°C",
                            f"Humidity: {data['humidity']}%",
                            f"Wind: {data['wind_speed']} Km/h, {data['wind_degree']}° Degrees",
                            f"Visibility: {data['visability'] / 1000} Km",
                            f"Pressure: {data['pressure'] / 1000} hPa",
                            f"Sea Level: {data['sea_level']}",
                            f"Sunrise: {data['sunrise']} AM",
                            f"Sunset: {data['sunset']} PM",
                            ""
                        )
                    else:
                        self._update_ui(
                            city_index,
                            "Temperature: --°C",
                            "Condition: --",         
                            "Min/Max Temp: --",
                            "Feels Like: --",
                            "Humidity: --",
                            "Wind: --",
                            "Visibility: --",
                            "Pressure: --",
                            "Sea Level: --",
                            "Sunrise: --",
                            "Sunset: --",
                            "City not found"
                        )

                except Exception as e:
                    self._update_ui(city_index, "Temperature: --°C", "Condition: --", f"Error: {str(e)}")
        finally:
            self.is_refreshing = False
            self.view.enable_all_buttons()  # Re-enable buttons when done

    def _update_ui(
        self,
        city_index,
        temperature_text,
        condition_text,
        min_max_temp,
        feels_like,
        humidity,
        wind,
        visibility,
        pressure,
        sea_level,
        sunrise,
        sunset,
        error_message
        ):
        """Updates the UI safely from the main thread."""
        self.view.root.after(
            0,
            self._update_ui_safely,
            city_index,
            temperature_text,
            condition_text,
            min_max_temp,
            feels_like,
            humidity,
            wind,
            visibility,
            pressure,
            sea_level,
            sunrise,
            sunset,
            error_message
        )


    def _update_ui_safely(
        self,
        city_index,
        temperature_text,
        condition_text,
        min_max_temp,
        feels_like,
        humidity,
        wind,
        visibility,
        pressure,
        sea_level,
        sunrise,
        sunset,
        error_message
    ):
        """Updates the UI elements for a specific city."""
        self.view.update_temperature(city_index, temperature_text)
        self.view.update_condition(city_index, condition_text)
        self.view.update_min_max_tempreture(city_index, min_max_temp)
        self.view.update_feels_like(city_index, feels_like)
        self.view.update_humidity(city_index, humidity)
        self.view.update_wind(city_index, wind)
        self.view.update_visability(city_index, visibility)
        self.view.update_pressure(city_index, pressure)
        self.view.update_sea_level(city_index, sea_level)
        self.view.update_sunrise(city_index, sunrise)
        self.view.update_sunset(city_index, sunset)
        if error_message:
            self.view.show_error(city_index, error_message)
        else:
            self.view.hide_error(city_index)
            # Update all additional data

