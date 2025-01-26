
class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Configure the refresh button to call the update_weather method
        self.view.refresh_button.config(command=self.create_update_weather_command())

    def create_update_weather_command(self):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather()

    def update_weather(self):
        """This is where the weather update process happens for each city."""
        for city_index, city_entry in enumerate(self.view.city_entries):
            city_name = city_entry.get()  # Get the city name from the entry
            data = self.model.fetch_weather(city_name)  # Fetch weather data for the city

            if data:
                # Update the temperature and condition labels for the current city
                self.view.update_temperature(city_index, f"Temperature: {data['temperature']}°C")
                self.view.update_condition(city_index, f"Condition: {data['weather_condition']}")
                self.view.hide_error(city_index)  # Hide the error label if data is found
            else:
                # Show error if no data is found for the current city
                self.view.show_error(city_index, "City not found")
                self.view.update_temperature(city_index, "Temperature: --°C")
                self.view.update_condition(city_index, "Condition: --")

        # After updating all cities, refresh the scroll region to reflect the layout change
        self.view.city_frame.update_idletasks()
        self.view.canvas.config(scrollregion=self.view.canvas.bbox("all"))