import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x500")  # Adjusted size for horizontal scrolling
        self.root.config(bg="#F1F1F1")  # Light grey background for the window

        # Title
        self.title_label = tk.Label(root, text="Weather Dashboard App", font=("Helvetica", 20, "bold"), fg="#4A90E2")
        self.title_label.pack(pady=20)  # Add padding for top space
        self.apply_font(self.title_label)

        # Create a frame for the scrollable area
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(pady=(10, 0), padx=20, fill="both", expand=True)

        # Create a Canvas widget for horizontal scrolling
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to hold city entries and weather data (horizontal layout)
        self.city_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.city_frame, anchor="nw")

        # Lists to hold dynamic widgets (city entries, labels)
        self.city_entries = []  # Will hold city input fields
        self.temperature_labels = []  # Will hold temperature labels
        self.condition_labels = []  # Will hold condition labels
        self.error_labels = []  # Will hold error labels
        self.remove_buttons = []  # Will hold remove buttons for each city
        self.city_frames = []  # Will hold city frames (including city input, weather labels, etc.)
        self.min_max_temperature_labels = []  # Min-Max temperature labels
        self.feels_like_labels = []  # Feels like temperature labels
        self.humidity_labels = []  # Humidity labels
        self.wind_labels = []  # Wind labels
        self.visibility_labels = []  # Visibility labels
        self.pressure_labels = []  # Pressure labels
        self.sea_level_labels = []  # Sea level labels
        self.sunrise_labels = []  # Sunrise labels
        self.sunset_labels = []  # Sunset labels

        # Initially create one city entry (without a remove button)
        self.is_first_city = True

        # Create a horizontal scrollbar for the Canvas using ttk (now below buttons)
        self.scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x", pady=(10, 20))  # Place scrollbar below buttons

        # Configure the canvas scrollbar
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Update scroll region
        self.city_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Customize the appearance of the scrollbar thumb
        style = ttk.Style()
        style.configure("TScrollbar", thickness=12)  # Adjust thickness here to make thumb smaller
        style.configure("TScrollbar.slider", sliderlength=40)  # Make the thumb smaller

        # Call add_city() after all initialization to ensure scrollbar is set
        self.add_city()

        # Frame to hold buttons (Add City and Refresh buttons)
        self.button_frame = tk.Frame(root, bg="#F1F1F1")
        self.button_frame.pack(pady=10, fill="x")

        # Button to add more cities
        self.add_city_button = tk.Button(self.button_frame, text="Add City", font=("Helvetica", 12), bg="#4A90E2", fg="white", command=self.add_city)
        self.add_city_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew", ipadx=8, ipady=4)

        # Refresh Button
        self.refresh_button = tk.Button(self.button_frame, text="Refresh All", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew", ipadx=8, ipady=4)

        # Ensure both buttons expand and are of equal width
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.apply_button_style(self.refresh_button)
        self.apply_button_style(self.add_city_button)

    def add_city(self):
        """Adds a new city entry, temperature, condition, and refresh button."""
        # Create a city frame for each city and add it to the city_frame
        city_frame = tk.Frame(self.city_frame, bd=2, relief="solid", padx=10, pady=5)
    
        # Determine the row and column for the grid
        row = 0  # All cities will be placed in the same row (row 0)
        column = len(self.city_entries)  # The column increments for each new city
    
        # Use grid to ensure proper alignment of cities
        city_frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
    
        # City Input Label
        city_label = tk.Label(city_frame, text="Enter City:", font=("Helvetica", 12), bg="#F1F1F1")
        city_label.grid(row=0, column=0, pady=(10, 5))
        self.apply_font(city_label)
    
        # City Input Field
        city_entry = tk.Entry(city_frame, font=("Helvetica", 14), relief="solid", bd=2, width=20)
        city_entry.insert(0, "London")  # Default text
        city_entry.grid(row=1, column=0, pady=10)
        self.apply_border(city_entry)
    
        # Error Label
        error_label = tk.Label(city_frame, text="", font=("Helvetica", 12), fg="red", bg="#F1F1F1")
        error_label.grid(row=4, column=0, pady=(5, 10))
        error_label.grid_forget()  # Hide by default
    
        # Weather Data Labels for the city
        weather_frame = tk.Frame(city_frame, bg="#F1F1F1")
        weather_frame.grid(row=2, column=0, columnspan=2, pady=10)  # Use grid for weather data layout
    
        # Row 1
        temperature_label = tk.Label(weather_frame, text="Temperature: --°C", font=("Helvetica", 12), bg="#F1F1F1")
        temperature_label.grid(row=0, column=0, pady=10)
    
        condition_label = tk.Label(weather_frame, text="Condition: --", font=("Helvetica", 12), bg="#F1F1F1")
        condition_label.grid(row=0, column=1, pady=10)
    
        # Row 2
        min_max_tempreture_label = tk.Label(weather_frame, text="--°C/--°C", font=("Helvetica", 12), bg="#F1F1F1")
        min_max_tempreture_label.grid(row=1, column=0, pady=10)
    
        feels_like_label = tk.Label(weather_frame, text="Feels Like: --°C", font=("Helvetica", 12), bg="#F1F1F1")
        feels_like_label.grid(row=1, column=1, pady=10)
    
        # Row 3
        humidity_label = tk.Label(weather_frame, text="Humidity: --%", font=("Helvetica", 12), bg="#F1F1F1")
        humidity_label.grid(row=2, column=0, pady=10)
    
        wind_label = tk.Label(weather_frame, text="Wind: -- Km/h, --° Degrees", font=("Helvetica", 12), bg="#F1F1F1")
        wind_label.grid(row=2, column=1, pady=10)

         # Row 4
        visability_label = tk.Label(weather_frame, text="Visability: -- Km", font=("Helvetica", 12), bg="#F1F1F1")
        visability_label.grid(row=3, column=0, pady=10)
        self.apply_font(visability_label)
        
        pressure_label = tk.Label(weather_frame, text="Pressure: -- hPa", font=("Helvetica", 12), bg="#F1F1F1")
        pressure_label.grid(row=3, column=1, pady=10)
        self.apply_font(pressure_label)
        
        # Row 5
        sea_level_label = tk.Label(weather_frame, text="Sea Level: --", font=("Helvetica", 12), bg="#F1F1F1")
        sea_level_label.grid(row=4, column=0, columnspan=2, pady=10)
        self.apply_font(sea_level_label)
        
        # Row 6
        sunrise_label = tk.Label(weather_frame, text="Sunrise: -- AM", font=("Helvetica", 12), bg="#F1F1F1")
        sunrise_label.grid(row=5, column=0, pady=10)
        self.apply_font(sunrise_label)
        
        sunset_label = tk.Label(weather_frame, text="Sunset: -- PM", font=("Helvetica", 12), bg="#F1F1F1")
        sunset_label.grid(row=5, column=1, columnspan=2, pady=10)
        self.apply_font(sunset_label)
    
        # Frame for condition label and image
        condition_frame = tk.Frame(city_frame, bg="#F1F1F1")
        condition_frame.grid(row=3, column=0, columnspan=2, pady=5)
    
        condition_image_label = tk.Label(condition_frame, bg="#F1F1F1")  # Label to display the condition image
        condition_image_label.grid(row=0, column=1)
    
        # Refresh Button
        refresh_button = tk.Button(city_frame, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        refresh_button.grid(row=5, column=0, pady=(10, 10))
    
        # Remove Button (only for non-first cities)
        if not self.is_first_city:
            remove_button = tk.Button(city_frame, text="Remove", font=("Helvetica", 12), bg="#FF4C4C", fg="white",
                                      command=lambda: self.remove_city(city_frame))
            remove_button.grid(row=6, column=0, pady=(10, 10))  # Pack the remove button
    
        self.is_first_city = False

        # Append to the lists
        self.city_entries.append(city_entry)
        self.error_labels.append(error_label)
        self.city_frames.append(city_frame)
        self.temperature_labels.append(temperature_label)
        self.condition_labels.append(condition_label)
        self.min_max_temperature_labels.append(min_max_tempreture_label)
        self.feels_like_labels.append(feels_like_label)
        self.humidity_labels.append(humidity_label)
        self.wind_labels.append(wind_label)
        self.visibility_labels.append(visability_label)  # Placeholder for now
        self.pressure_labels.append(pressure_label)  # Placeholder for now
        self.sea_level_labels.append(sea_level_label)  # Placeholder for now
        self.sunrise_labels.append(sunrise_label)  # Placeholder for now
        self.sunset_labels.append(sunset_label)  # Placeholder for now
    
        # Update the scroll region and handle scrollbar visibility
        self.update_scroll_region()



    def remove_city(self, city_frame):
        """Removes the city and its associated components, including the remove button."""
        try:
            # Find the index of the city frame in the list
            index = self.city_frames.index(city_frame)

            # Remove the "Remove" button from the list before destroying the city frame
            if index < len(self.remove_buttons):
                self.remove_buttons.pop(index)  # Remove the remove button from the list

            # Remove the city frame and its associated widgets
            city_frame.destroy()

            # After removal, update the lists
            self.city_frames.pop(index)
            self.city_entries.pop(index)
            self.error_labels.pop(index)

            # Shift all subsequent cities left to fill the gap
            for i in range(index, len(self.city_entries)):
                # Move each city frame to the left (to the previous column)
                self.city_frames[i].grid_forget()  # Remove the old position
                self.city_frames[i].grid(row=0, column=i, padx=10, pady=5, sticky="nsew")  # Reposition

            # Update the scroll region and handle scrollbar visibility
            self.update_scroll_region()

        except ValueError:
            print("City frame not found in the list.")

    def update_scroll_region(self):
        """Updates the scroll region and adjusts the scrollbar visibility."""
        # Update the scroll region to the new city frame size
        self.city_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Check if the content fits within the visible area
        if self.canvas.bbox("all")[2] <= self.canvas.winfo_width():
            # If the content width is less than or equal to the canvas width, hide the scrollbar
            self.scrollbar.pack_forget()
        else:
            # If the content overflows, show the scrollbar
            if not self.scrollbar.winfo_ismapped():  # Only show if not already visible
                self.scrollbar.pack(side="bottom", fill="x", pady=(10, 20))

    def update_weather_data(self, city_index, weather_data):
        """Update weather data labels for a given city."""
        self.update_temperature(city_index, weather_data["temperature"])
        self.update_condition(city_index, weather_data["condition"])
        self.update_min_max_tempreture(city_index, weather_data["min_max_temp"])
        self.update_feels_like(city_index, weather_data["feels_like"])
        self.update_humidity(city_index, weather_data["humidity"])
        self.update_wind(city_index, weather_data["wind"])
        self.update_visability(city_index, weather_data["visibility"])
        self.update_pressure(city_index, weather_data["pressure"])
        self.update_sea_level(city_index, weather_data["sea_level"])
        self.update_sunrise(city_index, weather_data["sunrise"])
        self.update_sunset(city_index, weather_data["sunset"])

    def update_temperature(self, city_index, text):
        """Update the temperature label."""
        temperature_label = self.temperature_labels[city_index]
        temperature_label.config(text=text)

    def update_condition(self, city_index, text):
        """Update the condition label."""
        condition_label = self.condition_labels[city_index]
        condition_label.config(text=text)

    def update_min_max_tempreture(self, city_index, text):
        """Update the min/max temperature label."""
        min_max_tempreture_label = self.min_max_temperature_labels[city_index]
        min_max_tempreture_label.config(text=text) 

    def update_feels_like(self, city_index, text):
        """Update the feels like temperature label."""
        feels_like_label = self.feels_like_labels[city_index]
        feels_like_label.config(text=text)

    def update_humidity(self, city_index, text):
        """Update the humidity label."""
        humidity_label = self.humidity_labels[city_index]
        humidity_label.config(text=text)

    def update_wind(self, city_index, text):
        """Update the wind speed and direction label."""
        wind_label = self.wind_labels[city_index]
        wind_label.config(text=text) 

    def update_visability(self, city_index, text):
        """Update the visibility label."""
        visibility_label = self.visibility_labels[city_index]
        visibility_label.config(text=text)

    def update_pressure(self, city_index, text):
        """Update the pressure label."""
        pressure_label = self.pressure_labels[city_index]
        pressure_label.config(text=text)

    def update_sea_level(self, city_index, text):
        """Update the sea level label."""
        sea_level_label = self.sea_level_labels[city_index]
        sea_level_label.config(text=text)

    def update_sunrise(self, city_index, text):
        """Update the sunrise label."""
        sunrise_label = self.sunrise_labels[city_index]
        sunrise_label.config(text=text) 

    def update_sunset(self, city_index, text):
        """Update the sunset label."""
        sunset_label = self.sunset_labels[city_index]
        sunset_label.config(text=text) 

    def apply_font(self, widget):
        """Applies the general font style."""
        widget.config(font=("Helvetica", 12))

    def apply_border(self, entry_widget):
        """Applies border style to the entry widget."""
        entry_widget.config(bd=2, relief="solid")

    def apply_button_style(self, button):
        """Applies consistent style to all buttons."""
        button.config(width=20)

    def show_error(self, city_index, error_message):
        """Displays error message for the city at city_index."""
        self.error_labels[city_index].config(text=error_message)
        self.error_labels[city_index].grid(row=4, column=0)  # Make the error label visible

    def hide_error(self, city_index):
        """Hides the error message for the city at city_index."""
        self.error_labels[city_index].grid_forget()

    def get_city_name(self, city_index):
        """Returns the city name from the entry field."""
        return self.city_entries[city_index].get()

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
        button.config(font=("Helvetica", 12, "bold"), relief="raised", height=1, width=12)
        button.config(activebackground="#357ABD", activeforeground="white")
