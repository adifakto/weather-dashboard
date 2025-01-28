
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
                        self._update_ui(city_index, f"Temperature: {data['temperature']}°C", f"Condition: {data['weather_condition']}", "")
                    else:
                        self._update_ui(city_index, "Temperature: --°C", "Condition: --", "City not found")
                except Exception as e:
                    self._update_ui(city_index, "Temperature: --°C", "Condition: --", f"Error: {str(e)}")
        finally:
            self.is_refreshing = False
            self.view.enable_all_buttons()  # Re-enable buttons when done

    def _update_ui(self, city_index, temperature_text, condition_text, error_message):
        """Updates the UI safely from the main thread."""
        self.view.root.after(0, self._update_ui_safely, city_index, temperature_text, condition_text, error_message)

    def _update_ui_safely(self, city_index, temperature_text, condition_text, error_message):
        """Updates the UI elements for a specific city."""
        self.view.update_temperature(city_index, temperature_text)
        self.view.update_condition(city_index, condition_text)
        if error_message:
            self.view.show_error(city_index, error_message)
        else:
            self.view.hide_error(city_index)
