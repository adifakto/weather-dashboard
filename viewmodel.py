class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.refresh_button.config(command=self.create_update_weather_command())

    def create_update_weather_command(self):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather()

    def update_weather(self):
        """This is where the weather update process happens."""
        city_name = self.view.city_menu.get()
        data = self.model.fetch_weather(city_name)

        if data:
            self.view.update_temperature(f"Temperature: {data['temperature']}°C")
            self.view.update_condition(f"Condition: {data['weather_condition']}")
        else:
            self.view.show_error("Failed to fetch weather data")