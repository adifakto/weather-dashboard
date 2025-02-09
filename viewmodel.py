from threading import Thread, Lock
import datetime

class WeatherViewModel:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_refreshing = False
        self.lock = Lock()  # Add a lock for thread safety
        
        # Bind buttons to methods
        self.view.add_city_button.config(command=self.add_city_if_not_refreshing)
        self.view.refresh_button.config(command=self.create_update_weather_command)

        """Assign the refresh button to use the weather update process"""     
           
    def add_city_if_not_refreshing(self):
        """Adds a city only if not currently refreshing."""
        if not self.is_refreshing:
            self.view.add_city()
            
    def create_update_weather_command(self):
        """Updates weather data for all cities in a background thread."""
        if self.is_refreshing:
            return  # Prevent multiple refreshes

        self.is_refreshing = True
        self.view.disable_all_buttons()  # Disable buttons immediately

        # Start a background thread to fetch weather data
        Thread(target=self.update_weather, daemon=True).start()


    def update_weather(self):
        # if self.is_refreshing:
        #     return
        
        self.is_refreshing = True
        self.view.disable_all_buttons()  # Disable buttons immediately
        """This is where the weather update process happens for each city."""
        for city_index, city_entry in enumerate(self.view.city_entries):
            city_name = city_entry.get()  # Get the city name from the entry
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
                self.view.update_visability(city_index, f"Visability: {data['visability']/1000} Km")
                self.view.update_pressure(city_index, f"Pressure: {data['pressure']/1000} hPa")
                self.view.update_sea_level(city_index, f"Sea Level: {data['sea_level']}")
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
                self.view.update_wind(city_index, "Wind: -- Km/h, --° Degrees")
                self.view.update_visability(city_index, "Visability: -- Km")
                self.view.update_pressure(city_index, "Pressure: -- hPa")
                self.view.update_sea_level(city_index, "Sea Level: --")
                self.view.update_sunrise(city_index, "Sunrise: -- AM")
                self.view.update_sunset(city_index, "Sunset: -- PM")

                # Loop through error_labels and call pack_forget on each
                for error_label in self.view.error_labels:
                    error_label.pack_forget()
            
        self.is_refreshing = False
        self.view.enable_all_buttons()  # Re-enable buttons when done

        # After updating all cities, refresh the scroll region to reflect the layout change
        self.view.city_frame.update_idletasks()
        self.view.canvas.config(scrollregion=self.view.canvas.bbox("all"))