class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Set up the callback for new cities
        self.view.on_city_added = self.on_new_city_added

        # Configure initial refresh buttons
        for idx, button in enumerate(self.view.refresh_buttons):
            self.configure_refresh_button(idx)

        # Configure the refresh all button
        self.view.refresh_all_button.config(command=self.update_weather_all_command())

    def on_new_city_added(self, city_index):
        """Callback method when a new city is added."""
        self.configure_refresh_button(city_index)

    def configure_refresh_button(self, idx):
        """Configures the refresh button for a specific city index."""
        if idx < len(self.view.refresh_buttons):
            self.view.refresh_buttons[idx].config(command=self.update_weather_command(idx))

    def update_weather_command(self, idx):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather(idx)

    def update_weather_all_command(self):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather_all()

    def update_weather(self, city_index):
        city_name = self.view.city_entries[city_index].get()
        data = self.model.fetch_weather(city_name)  # Fetch weather data for the city

        if data:
            # Pass the city_index along with the data to the update methods
            self.view.hide_error(city_index)
            self.view.update_temperature(city_index, f"Temperature: {data['temperature']}°C")
            self.view.update_condition(city_index, f"Condition: {data['weather_condition']}")
            self.view.update_min_max_tempreture(city_index, f"{data['min_tempreture']}°C/{data['max_tempreture']}°C")
            self.view.update_feels_like(city_index, f"Feels Like: {data['feels_like']}°C")
            self.view.update_humidity(city_index, f"Humidity: {data['humidity']}%")
            self.view.update_wind(city_index, f"Wind: {data['wind_speed']} Km/h, {data['wind_degree']}° Degrees")
            self.view.update_visability(city_index, f"Visability: {data['visability'] / 1000} Km")
            self.view.update_pressure(city_index, f"Pressure: {data['pressure'] / 1000} hPa")
            self.view.update_sea_level(city_index, f"Sea Level: {data['sea_level']}")
            self.view.update_sunrise(city_index, f"Sunrise: {data['sunrise']} AM")
            self.view.update_sunset(city_index, f"Sunset: {data['sunset']} PM")

            # Loop through error_labels and call pack_forget on each
            for error_label in self.view.error_labels:
                error_label.pack_forget()
        else:
            self.view.show_error(city_index, "City not found")
            self.view.update_temperature(city_index, "Temperature: -- °C")
            self.view.update_condition(city_index, "Condition: --")
            self.view.update_min_max_tempreture(city_index, "--°C/--°C")
            self.view.update_feels_like(city_index, "Feels Like: --°C")
            self.view.update_humidity(city_index, "Humidity: --%")
            self.view.update_wind(city_index, "Wind: -- Km/h, --° Degrees")
            self.view.update_visability(city_index, "Visability: -- Km")
            self.view.update_pressure(city_index, "Pressure: -- hPa")
            self.view.update_sea_level(city_index, "Sea Level: --")
            self.view.update_sunrise(city_index, "Sunrise: -- AM")
            self.view.update_sunset(city_index, "Sunset: -- PM")

            # Loop through error_labels and call pack_forget on each
            for error_label in self.view.error_labels:
                error_label.pack_forget()

    def update_weather_all(self):
        """This is where the weather update process happens for each city."""
        for city_index, city_entry in enumerate(self.view.city_entries):
            city_name = city_entry.get()  # Get the city name from the entry
            data = self.model.fetch_weather(city_name)  # Fetch weather data for the city

            if data:
                # Pass the city_index along with the data to the update methods
                self.view.hide_error(city_index)
                self.view.update_temperature(city_index, f"Temperature: {data['temperature']}°C")
                self.view.update_condition(city_index, f"Condition: {data['weather_condition']}")
                self.view.update_min_max_tempreture(city_index,
                                                    f"{data['min_tempreture']}°C/{data['max_tempreture']}°C")
                self.view.update_feels_like(city_index, f"Feels Like: {data['feels_like']}°C")
                self.view.update_humidity(city_index, f"Humidity: {data['humidity']}%")
                self.view.update_wind(city_index, f"Wind: {data['wind_speed']} Km/h, {data['wind_degree']}° Degrees")
                self.view.update_visability(city_index, f"Visability: {data['visability'] / 1000} Km")
                self.view.update_pressure(city_index, f"Pressure: {data['pressure'] / 1000} hPa")
                self.view.update_sea_level(city_index, f"Sea Level: {data['sea_level']}")
                self.view.update_sunrise(city_index, f"Sunrise: {data['sunrise']} AM")
                self.view.update_sunset(city_index, f"Sunset: {data['sunset']} PM")

                # Loop through error_labels and call pack_forget on each
                for error_label in self.view.error_labels:
                    error_label.pack_forget()
            else:
                self.view.show_error(city_index, "City not found")
                self.view.update_temperature(city_index, "Temperature: -- °C")
                self.view.update_condition(city_index, "Condition: --")
                self.view.update_min_max_tempreture(city_index, "--°C/--°C")
                self.view.update_feels_like(city_index, "Feels Like: --°C")
                self.view.update_humidity(city_index, "Humidity: --%")
                self.view.update_wind(city_index, "Wind: -- Km/h, --° Degrees")
                self.view.update_visability(city_index, "Visability: -- Km")
                self.view.update_pressure(city_index, "Pressure: -- hPa")
                self.view.update_sea_level(city_index, "Sea Level: --")
                self.view.update_sunrise(city_index, "Sunrise: -- AM")
                self.view.update_sunset(city_index, "Sunset: -- PM")

                # Loop through error_labels and call pack_forget on each
                for error_label in self.view.error_labels:
                    error_label.pack_forget()

        # After updating all cities, refresh the scroll region to reflect the layout change
        self.view.city_frame.update_idletasks()
        self.view.canvas.config(scrollregion=self.view.canvas.bbox("all"))