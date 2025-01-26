import tkinter as tk

class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("550x600")  # Adjust the window size
        self.root.config(bg="#F1F1F1")  # Light grey background for the window

        # Title
        self.title_label = tk.Label(root, text="Weather Dashboard App", font=("Helvetica", 20, "bold"), fg="#4A90E2")
        self.title_label.pack(pady=20)  # Add padding for top space
        self.apply_font(self.title_label)
        
        # City Input Label
        self.city_label = tk.Label(root, text="Enter City:", font=("Helvetica", 12), bg="#F1F1F1")
        self.city_label.pack(pady=(10, 5))  # Add top and bottom padding
        self.apply_font(self.city_label)

        # City Input Field
        self.city_entry = tk.Entry(root, font=("Helvetica", 14), relief="solid", bd=2, width=20)
        self.city_entry.insert(0, "London")  # Default text
        self.city_entry.pack(pady=10, padx=20)  # Add padding around the entry widget
        self.apply_border(self.city_entry)

        # Error Label
        self.error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red", bg="#F1F1F1")
        self.error_label.pack(pady=(5, 10))  # Add padding above the weather info
        self.error_label.pack_forget()  # Hide by default

        # Weather Data Labels - Two Rows Layout to contain all the weather-related labels
        self.weather_frame = tk.Frame(root, bg="#F1F1F1")
        self.weather_frame.pack(pady=10)  # Add padding around the weather info

         # Row 1
        self.temperature_label = tk.Label(self.weather_frame, text="Temperature: --°C", font=("Helvetica", 12), bg="#F1F1F1")
        self.temperature_label.grid(row=0, column=0, pady=10)  # Place in row 0, column 0
        self.apply_font(self.temperature_label)
        
        self.condition_label = tk.Label(self.weather_frame, text="Condition: --", font=("Helvetica", 12), bg="#F1F1F1")
        self.condition_label.grid(row=0, column=1, columnspan=2, pady=10)  # Place in row 0, column 1
        self.apply_font(self.condition_label)
        
        # Row 2
        self.min_max_tempreture_label = tk.Label(self.weather_frame, text="--°C/--°C", font=("Helvetica", 12), bg="#F1F1F1")
        self.min_max_tempreture_label.grid(row=1, column=0, pady=10)
        self.apply_font(self.min_max_tempreture_label)

        self.feels_like_label = tk.Label(self.weather_frame, text="Feels Like: --°C", font=("Helvetica", 12), bg="#F1F1F1")
        self.feels_like_label.grid(row=1, column=1, pady=10)
        self.apply_font(self.feels_like_label)
        
        # Row 3
        self.humidity_label = tk.Label(self.weather_frame, text="Humidity: --%")
        self.humidity_label.grid(row=2, column=0, pady=10)
        self.apply_font(self.humidity_label)
        
        self.wind_label = tk.Label(self.weather_frame, text="Wind: -- Km/h, --° Degrees")
        self.wind_label.grid(row=2, column=1, pady=10)
        self.apply_font(self.wind_label)
        
        # Row 4
        self.visability_label = tk.Label(self.weather_frame, text="Visability: -- Km")
        self.visability_label.grid(row=3,column=0, pady=10)
        self.apply_font(self.visability_label)
        
        self.pressure_label = tk.Label(self.weather_frame, text="Pressure: -- hPa")
        self.pressure_label.grid(row=3, column=1, pady=10)
        self.apply_font(self.pressure_label)
        
        # Row 5
        self.sea_level_label = tk.Label(self.weather_frame, text="Sea Level: --")
        self.sea_level_label.grid(row=4, column=0, columnspan=2, pady=10)
        self.apply_font(self.sea_level_label)
        
        # Row 6
        self.sunrise_label = tk.Label(self.weather_frame, text="Sunrise: -- AM")
        self.sunrise_label.grid(row=5, column=0, pady=10)
        self.apply_font(self.sunrise_label)
        
        self.sunset_label = tk.Label(self.weather_frame, text="Sunset: -- PM")
        self.sunset_label.grid(row=5, column=1, pady=10)
        self.apply_font(self.sunset_label)

        # Refresh Button
        self.refresh_button = tk.Button(root, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        self.refresh_button.pack(pady=10)
        self.apply_button_style(self.refresh_button)

    def update_temperature(self, text):
        self.temperature_label.config(text=text)
        self.apply_decorations(self.temperature_label)

    def update_condition(self, text):
        self.condition_label.config(text=text)
        
    def update_min_max_tempreture(self, text):
        self.min_max_tempreture_label.config(text=text)
        
    def update_feels_like(self, text):
        self.feels_like_label.config(text=text)
        
    def update_humidity(self, text):
        self.humidity_label.config(text=text)
        
    def update_wind(self, text):
        self.wind_label.config(text=text)
        
    def update_visability(self, text):
        self.visability_label.config(text=text)
        
    def update_pressure(self, text):
        self.pressure_label.config(text=text)
        
    def update_sea_level(self, text):
        self.sea_level_label.config(text=text)
        
    def update_sunrise(self, text):
        self.sunrise_label.config(text=text)
        
    def update_sunset(self, text):
        self.sunset_label.config(text=text)
        

    def show_error(self, error_message):
        """Displays error message above the weather info."""
        self.error_label.config(text=error_message)
        self.error_label.pack()  # Make the error label visible

    def apply_decorations(self, label):
        self.apply_color(label)

    # Small decoration functions for styling
    def apply_font(self, widget):
        widget.config(font=("Helvetica", 14), fg="#333333")  # Apply font and text color

    def apply_color(self, label):
        label.config(fg="#333333")  # Apply a dark color for text for better readability

    def apply_border(self, widget):
        widget.config(bd=2, relief="solid", width=20)  # Add border to input field

    def apply_button_style(self, button):
        button.config(font=("Helvetica", 12, "bold"), relief="raised", height=2, width=15)
        button.config(activebackground="#357ABD", activeforeground="white")  # Add hover effect
