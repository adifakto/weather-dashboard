import threading
import datetime

class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_refreshing = False

        # Set up the callback for new cities
        self.view.on_city_added = self.on_new_city_added
        
        # self.view.add_city_button.config(command=self.add_city_if_not_refreshing) # depreicated, functionallity moved to method disable_all_buttons

        # Configure refresh button of initial city
        self.configure_refresh_button(0)

        # Configure the refresh all button
        self.view.refresh_all_button.configure(command=self.update_weather_all_command())
    
    def on_new_city_added(self, city_frame):
        city_index = self.view.city_frames.index(city_frame)
        self.configure_refresh_button(city_index)
        
    def configure_refresh_button(self, city_index):
        """Configures the refresh button for a specific city index."""
        self.view.refresh_buttons[city_index].configure(command=self.update_weather_command(city_index))

    def update_weather_command(self, city_index):
        """Creates the command directly as a callable (lambda function)."""
        return lambda: self.update_weather_aux(city_index)
    
    def update_weather_aux(self, city_index):
        city_frame = self.view.city_frames[city_index]
        
        def update_weather_aux_aux(city_index):
            self.view.disable_remove_button(city_frame)

            self.update_weather(city_index)
            
            self.view.enable_remove_button(city_frame)
        
        
            
        threading.Thread(target=lambda: update_weather_aux_aux(city_index), daemon=True).start()
        
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
            self.view.update_wind(city_index, f"Wind: {data['wind_speed']} m/s, {data['wind_degree']}° Degrees")
            self.view.update_visibility(city_index, f"visibility: {data['visibility'] / 1000} Km")
            self.view.update_pressure(city_index, f"Pressure: {data['pressure'] / 1000} hPa")
            self.view.update_clouds(city_index, f"Clouds: {data['clouds']}%")
            self.view.update_sunrise(city_index, f"Sunrise: {datetime.datetime.fromtimestamp(data['sunrise'], tz=datetime.timezone.utc).strftime('%H:%M AM')}")
            self.view.update_sunset(city_index, f"Sunset: {datetime.datetime.fromtimestamp(data['sunset'], tz=datetime.timezone.utc).strftime('%H:%M PM')}")

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
            self.view.update_wind(city_index, "Wind: -- m/s, --° Degrees")
            self.view.update_visibility(city_index, "Visibility: -- Km")
            self.view.update_pressure(city_index, "Pressure: -- hPa")
            self.view.update_clouds(city_index, "Clouds: -- %")
            self.view.update_sunrise(city_index, "Sunrise: -- AM")
            self.view.update_sunset(city_index, "Sunset: -- PM")

            # Loop through error_labels and call pack_forget on each
            for error_label in self.view.error_labels:
                error_label.pack_forget()
                
    def update_weather_all(self):
        if self.is_refreshing:
            return  # Prevent multiple refreshes
        
        def update_weather_all_aux():
            self.is_refreshing = True
            self.view.disable_all_buttons()  # Disable all buttons immediately
        
            for i in range(0, len(self.view.city_entries)):
                self.update_weather(i)
                
            self.is_refreshing = False
            self.view.enable_all_buttons()  # Re-enable buttons after fetching is done   
        
        # Run the fetching process in a separate thread
        threading.Thread(target=update_weather_all_aux, daemon=True).start() 
        