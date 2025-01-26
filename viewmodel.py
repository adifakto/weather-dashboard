class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.refresh_request_id = 0 # Counter to track the most recent request

        """Assign the refresh button to use the weather update process"""        
        self.view.refresh_button.config(command=self.create_update_weather_command())

    def create_update_weather_command(self):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather()

    def update_weather(self):
        """This is where the weather update process happens."""
        city_name = self.view.city_entry.get()
        data = self.model.fetch_weather(city_name)

        if data:
            self.view.update_temperature(f"Temperature: {data['temperature']}°C")
            self.view.update_condition(f"Condition: {data['weather_condition']}")
            self.view.update_min_max_tempreture(f"{data['min_tempreture']}°C/{data['max_tempreture']}°C")
            self.view.update_feels_like(f"Feels Like: {data['feels_like']}°C")
            self.view.update_humidity(f"Humidity: {data['humidity']}%")
            self.view.update_wind(f"Wind: {data['wind_speed']} Km/h, {data['wind_degree']}° Degrees")
            self.view.update_visability(f"Visability: {data['visability']/1000} Km")
            self.view.update_pressure(f"Pressure: {data['pressure']/1000} hPa")
            self.view.update_sea_level(f"Sea Level: {data['sea_level']}")
            self.view.update_sunrise(f"Sunrise: {data['sunrise']} AM")
            self.view.update_sunset(f"Sunset: {data['sunset']} PM")
            self.view.error_label.pack_forget()
        else:
            self.view.show_error("city not found")
            self.view.update_temperature(f"Temperature: -- °C")
            self.view.update_condition(f"Condition: --")
            self.view.update_min_max_tempreture(f"--°C/--°C")
            self.view.update_feels_like(f"Feels Like: --°C")
            self.view.update_humidity(f"Humidity: --%")
            self.view.update_wind(f"Wind: -- Km/h, --° Degrees")
            self.view.update_visability(f"Visability: -- Km")
            self.view.update_pressure(f"Pressure: -- hPa")
            self.view.update_sea_level(f"Sea Level: --")
            self.view.update_sunrise(f"Sunrise: -- AM")
            self.view.update_sunset(f"Sunset: -- PM")
            self.view.error_label.pack_forget()