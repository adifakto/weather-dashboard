import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

class WeatherView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure Window
        self.title("Weather Dashboard")
        self.geometry("1200x800")  # Adjusted for better layout
        self.minsize(800, 800)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
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
        self.clouds_labels = []  # Clouds labels
        self.sunrise_labels = []  # Sunrise labels
        self.sunset_labels = []  # Sunset labels
        self.refresh_buttons = []  # Refresh buttons
        self.gif_labels = [] # gifs for the weather condotion
        self.weather_gifs = { # Weather GIFs (stored as a dictionary for different conditions)
            "Clear": "pics/clear.gif",
            "Clouds": "pics/clouds.gif",
            "Rain": "pics/rain.gif",
            "Drizzle": "pics/drizzle.gif",
            "Thunderstorm": "pics/storm.gif",
            "Snow": "pics/snow.gif",
            "Mist": "pics/mist.gif",
            "Fog": "pics/fog.gif",
            "Haze": "pics/fog.gif"
        }
        self.current_gif = None
        
        # ============ MAIN FRAME ============
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # ============ HEADER ============
        self.header_label = ctk.CTkLabel(self.main_frame, text="Weather Dashboard", font=("Helvetica Bold", 24, "bold"))
        self.header_label.pack(pady=10)

        # ============ SCROLLABLE AREA (Canvas + Inner Frame) ============
        self.scrollable_frame = ctk.CTkFrame(self.main_frame)
        self.scrollable_frame.pack(padx=20, pady=(10, 0), fill="both",  expand=True)
        
        # ============ Canvas for horizontal scrolling ============
        self.canvas = ctk.CTkCanvas(self.scrollable_frame, bg="#222", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Frame to hold city entries and weather data
        self.city_frame = ctk.CTkFrame(self.canvas, bg_color="#222")
        self.city_window = self.canvas.create_window((0, 0), window=self.city_frame, anchor="nw")
        
        # ============ Scrollbar ============
        self.scrollbar = ctk.CTkScrollbar(self.scrollable_frame, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbar.set) # connect canvas scrolling to scrollbar

        # ============ ADD CITY, REFRESH ALL BUTTONS ============
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent") # frame to hold the buttons
        self.button_frame.pack(fill="x", pady=10)
        
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.add_city_button = ctk.CTkButton(self.button_frame, text="Add City", command=self.add_city, font=("Helvetica", 20))
        self.add_city_button.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.refresh_all_button = ctk.CTkButton(self.button_frame, text="Refresh All", font=("Helvetica", 20))
        self.refresh_all_button.grid(row=0, column=1, padx=10, pady=(10, 0))
        
        # ============ LIGHT/DARK MODE TOGGLE BUTTON ============
        self.dark_mode = True  # Start in dark mode

        # Load images
        self.dark_mode_icon = ctk.CTkImage(light_image=Image.open("pics/dark_mode.png"), dark_image=Image.open("pics/dark_mode.png"), size=(30, 30))
        self.light_mode_icon = ctk.CTkImage(light_image=Image.open("pics/light_mode.png"), dark_image=Image.open("pics/light_mode.png"), size=(30, 30))

        self.theme_button = ctk.CTkButton(self.button_frame, width=30, height=30, text="", corner_radius=5, bg_color="transparent", fg_color="transparent", hover=False, font=("Helvetica", 18), image=self.dark_mode_icon, command=self.toggle_theme)
        self.theme_button.grid(row=1, column=2, padx=10, pady=(10, 0))

        # Callback mechanism for adding functionality to the refresh button when a new city is added
        self.on_city_added = None

        # Initially create one city entry (without a remove button)
        self.is_first_city = True
        
        self.city_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.add_city()
        self.center_city_frame()
        
        self.city_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.bind("<Configure>", lambda e: self.center_city_frame())
    
    def add_city(self):

        # Determine the row and column for the grid
        row = 0  # All cities will be placed in the same row (row 0)
        column = len(self.city_entries)  # The column increments for each new city

        # Arrange an inner city frame in the grid
        city_frame = ctk.CTkFrame(self.city_frame, fg_color="transparent")
        city_frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")

        # City Input Label
        city_label = ctk.CTkLabel(city_frame, text="Enter City:", font=("Helvetica", 14), width=20)
        city_label.grid(row=0, column=0, pady=(10, 5))

        # City Input Field
        city_entry = ctk.CTkEntry(city_frame, font=("Helvetica", 14), border_width=2, width=100)
        city_entry.insert(0, "London")  # Default text
        city_entry.grid(row=1, column=0, pady=10)

        # Error Label
        error_label = ctk.CTkLabel(city_frame, text="", font=("Helvetica", 14), fg_color="red", bg_color="#F1F1F1")
        error_label.grid(row=4, column=0, pady=(5, 10))
        error_label.grid_forget()  # Hide by default

        # Weather Data Labels for the city
        weather_frame = ctk.CTkFrame(city_frame)
        weather_frame.grid(row=2, column=0, columnspan=2, pady=10)  # Use grid for weather data layout

        # Row 1
        temperature_label = ctk.CTkLabel(weather_frame, text="Temperature: --°C", font=("Helvetica", 14))
        temperature_label.grid(row=0, column=0, pady=10)

        condition_label = ctk.CTkLabel(weather_frame, text="Condition: --", font=("Helvetica", 14))
        condition_label.grid(row=0, column=1, pady=10)
        
        # Weather Condition Image (to be placed to the right of the condition label)
        gif_label = ctk.CTkLabel(weather_frame, text="" ,bg_color="transparent")  # Label to display the condition image
        gif_label.grid(row=0, column=2, pady=10)  # Place the image to the right of the label

        # Row 2
        min_max_tempreture_label = ctk.CTkLabel(weather_frame, text="--°C/--°C", font=("Helvetica", 14))
        min_max_tempreture_label.grid(row=1, column=0, pady=10)

        feels_like_label = ctk.CTkLabel(weather_frame, text="Feels Like: --°C", font=("Helvetica", 14))
        feels_like_label.grid(row=1, column=1, pady=10)

        # Row 3
        humidity_label = ctk.CTkLabel(weather_frame, text="Humidity: --%", font=("Helvetica", 14))
        humidity_label.grid(row=2, column=0, pady=10)

        wind_label = ctk.CTkLabel(weather_frame, text="Wind: -- m/s, --° Degrees", font=("Helvetica", 14))
        wind_label.grid(row=2, column=1, pady=10)

        # Row 4
        visibility_label = ctk.CTkLabel(weather_frame, text="Visibility: -- Km", font=("Helvetica", 14))
        visibility_label.grid(row=3, column=0, pady=10)
        
        pressure_label = ctk.CTkLabel(weather_frame, text="Pressure: -- hPa", font=("Helvetica", 14))
        pressure_label.grid(row=3, column=1, pady=10)

        # Row 5
        clouds_label = ctk.CTkLabel(weather_frame, text="Clouds: --", font=("Helvetica", 14))
        clouds_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Row 6
        sunrise_label = ctk.CTkLabel(weather_frame, text="Sunrise: -- AM", font=("Helvetica", 14))
        sunrise_label.grid(row=5, column=0, pady=10)

        sunset_label = ctk.CTkLabel(weather_frame, text="Sunset: -- PM", font=("Helvetica", 14))
        sunset_label.grid(row=5, column=1, columnspan=2, pady=10)
        
        # Refresh Button
        refresh_button = ctk.CTkButton(city_frame, text="Refresh", font=("Helvetica", 12), fg_color="#4A90E2")
        refresh_button.grid(row=5, column=0, pady=(10, 10))

        # Remove Button (only for non-first cities)
        if not self.is_first_city:
            remove_button = ctk.CTkButton(city_frame, text="Remove", font=("Helvetica", 12), fg_color="#FF4C4C",
                                    command=lambda: self.remove_city(city_frame))
            remove_button.grid(row=6, column=0, pady=(10, 10))  # Pack the remove button
            self.remove_buttons.append(remove_button)

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
        self.visibility_labels.append(visibility_label)
        self.pressure_labels.append(pressure_label)
        self.clouds_labels.append(clouds_label)
        self.sunrise_labels.append(sunrise_label)
        self.sunset_labels.append(sunset_label)
        self.refresh_buttons.append(refresh_button)
        self.gif_labels.append(gif_label)

        # Update the scroll region and handle scrollbar visibility
        self.update_scroll_region()

        # Notify callback about the new city
        if self.on_city_added:
            self.on_city_added(city_frame)

    def remove_city(self, city_frame):
        """Removes the city and its associated components."""
        try:
            index = self.city_frames.index(city_frame)

            # Destroy all widgets in the city frame
            for widget in city_frame.winfo_children():
                widget.destroy()
                
            # Remove the city frame from the grid
            city_frame.grid_forget()

            # Remove the city frame and its associated components from the lists
            self.city_frames.pop(index)
            self.city_entries.pop(index)
            self.error_labels.pop(index)
            self.temperature_labels.pop(index)
            self.condition_labels.pop(index)
            self.min_max_temperature_labels.pop(index)
            self.feels_like_labels.pop(index)
            self.humidity_labels.pop(index)
            self.wind_labels.pop(index)
            self.visibility_labels.pop(index)
            self.pressure_labels.pop(index)
            self.clouds_labels.pop(index)
            self.sunrise_labels.pop(index)
            self.sunset_labels.pop(index)
            self.refresh_buttons.pop(index)
            self.remove_buttons.pop(index - 1)
            self.gif_labels.pop(index)

            # Shift remaining cities (update their grid position)
            for i in range(index, len(self.city_entries)):
                # Reset the grid row and column for the remaining cities
                self.city_frames[i].grid_forget()  # Remove from the current position
                self.city_frames[i].grid(row=0, column=i, padx=10, pady=5, sticky="nsew")  # Place at new position
                if self.on_city_added:
                    self.on_city_added(self.city_frames[i]) # update the callback with the new city_frame

            # Update the scroll region
            self.update_scroll_region()

        except ValueError:
            print("City frame not found in the list.")

    def toggle_theme(self):
        """Toggles between light and dark mode."""
        self.dark_mode = not self.dark_mode  # Toggle state
        new_mode = "dark" if self.dark_mode else "light"
        
        ctk.set_appearance_mode(new_mode)
        
        # Update light/dark mode button
        new_icon = self.dark_mode_icon if self.dark_mode else self.light_mode_icon
        self.theme_button.configure(text="", bg_color="transparent", fg_color="transparent", hover=False, font=("Helvetica", 18), image=new_icon)
        
        # Update colors
        new_bg = "#222" if self.dark_mode else "#EEE"  # Dark mode (gray) | Light mode (light gray)
        self.canvas.configure(bg=new_bg)
        self.city_frame.configure(bg_color=new_bg)
    
        # Force UI update
        self.update_idletasks()

    def center_city_frame(self):
        """Centers the city frame inside the canvas."""
        self.canvas.update_idletasks()  # Ensure layout updates before measuring
        
        canvas_width = self.canvas.winfo_width()
        frame_width = self.city_frame.winfo_reqwidth()
        
        canvas_height = self.canvas.winfo_height()
        frame_height = self.city_frame.winfo_reqheight()

        new_x = max((canvas_width - frame_width) // 2, 0)  # Ensure non-negative offset
        new_y = max((canvas_height - frame_height) // 2, 0)  # Ensure non-negative offset
        
        self.canvas.coords(self.city_window, new_x, new_y)  # Adjust window position
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_scroll_region(self):
        self.city_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        """Updates the scroll region and adjusts the scrollbar visibility."""
        if self.canvas.bbox("all")[2] <= self.canvas.winfo_width() or len(self.city_entries) == 1: # the or is added for the inital program start, because self.canvas.winfo_width() seems to not contain the right value until add city is clicked
            self.scrollbar.pack_forget()
        else:
            if not self.scrollbar.winfo_ismapped():
                self.scrollbar.pack(side="bottom", fill="x")

    def update_weather_data(self, city_index, weather_data):
        """Update weather data labels for a given city."""
        self.update_temperature(city_index, weather_data["temperature"])
        self.update_condition(city_index, weather_data["condition"])
        self.update_min_max_tempreture(city_index, weather_data["min_max_temp"])
        self.update_feels_like(city_index, weather_data["feels_like"])
        self.update_humidity(city_index, weather_data["humidity"])
        self.update_wind(city_index, weather_data["wind"])
        self.update_visibility(city_index, weather_data["visibility"])
        self.update_pressure(city_index, weather_data["pressure"])
        self.update_clouds(city_index, weather_data["clouds"])
        self.update_sunrise(city_index, weather_data["sunrise"])
        self.update_sunset(city_index, weather_data["sunset"])

    def update_temperature(self, city_index, text):
        """Update the temperature label."""
        temperature_label = self.temperature_labels[city_index]
        temperature_label.configure(text=text)

    def update_condition(self, city_index, text):
        """Update the condition label."""
        condition_label = self.condition_labels[city_index]
        condition_label.configure(text=text)
        
        # Get the condition text (after "Condition:")
        condition = text.split(":")[1].strip()

        # Get the image path for the weather condition
        image_path = self.weather_gifs.get(condition, None)

        if image_path:
            try:
                # Open the image using PIL
                self.current_image = Image.open(image_path)

                # Resize the image to fit the label (if needed)
                resized_image = self.current_image.resize((70, 70))  # Adjust size as needed
                image_display = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(70, 70))

                # Display the image by updating the image label
                self.gif_labels[city_index].configure(image=image_display)
                self.gif_labels[city_index].image = image_display  # Keep a reference to the image
            except Exception as e:
                # If there is an error loading the image, show an error message
                self.error_labels[city_index].configure(text=f"Error loading image: {e}")

                # Use grid instead of pack
                self.error_labels[city_index].grid(row=city_index, column=2)  # Adjust row/column as needed
        else:
            print("No matching image found.")

    def update_min_max_tempreture(self, city_index, text):
        """Update the min/max temperature label."""
        min_max_tempreture_label = self.min_max_temperature_labels[city_index]
        min_max_tempreture_label.configure(text=text) 

    def update_feels_like(self, city_index, text):
        """Update the feels like temperature label."""
        feels_like_label = self.feels_like_labels[city_index]
        feels_like_label.configure(text=text)

    def update_humidity(self, city_index, text):
        """Update the humidity label."""
        humidity_label = self.humidity_labels[city_index]
        humidity_label.configure(text=text)

    def update_wind(self, city_index, text):
        """Update the wind speed and direction label."""
        wind_label = self.wind_labels[city_index]
        wind_label.configure(text=text) 

    def update_visibility(self, city_index, text):
        """Update the visibility label."""
        visibility_label = self.visibility_labels[city_index]
        visibility_label.configure(text=text)

    def update_pressure(self, city_index, text):
        """Update the pressure label."""
        pressure_label = self.pressure_labels[city_index]
        pressure_label.configure(text=text)

    def update_clouds(self, city_index, text):
        """Update the sea level label."""
        clouds_label = self.clouds_labels[city_index]
        clouds_label.configure(text=text)

    def update_sunrise(self, city_index, text):
        """Update the sunrise label."""
        sunrise_label = self.sunrise_labels[city_index]
        sunrise_label.configure(text=text) 

    def update_sunset(self, city_index, text):
        """Update the sunset label."""
        sunset_label = self.sunset_labels[city_index]
        sunset_label.configure(text=text) 

    def show_error(self, city_index, error_message):
        """Displays error message for the city at city_index."""
        self.error_labels[city_index].configure(text=error_message)
        self.error_labels[city_index].grid(row=4, column=0)

    def hide_error(self, city_index):
        """Hides the error message for the city at city_index."""
        self.error_labels[city_index].grid_forget()

    def get_city_name(self, city_index):
        """Returns the city name from the entry field."""
        return self.city_entries[city_index].get()

    def disable_all_buttons(self):
        """Disables all buttons in the UI."""
        for button in self.refresh_buttons:
            if button.winfo_exists():  # Check if the widget still exists
                button.configure(state="disabled")
            
        for button in self.remove_buttons:
            if button.winfo_exists():  # Check if the widget still exists
                button.configure(state="disabled")
            
        self.refresh_all_button.configure(state="disabled")  # Disable the refresh all button
        self.add_city_button.configure(state="disabled")    # Disable the add city button

    def enable_all_buttons(self):
        """Enables all buttons in the UI."""
        for button in self.refresh_buttons:
            button.configure(state="normal")
        
        for button in self.remove_buttons:
            button.configure(state="normal")
        
        self.refresh_all_button.configure(state="normal")  # Re-enable the refresh all button
        self.add_city_button.configure(state="normal")    # Re-enable the add city button

    def disable_remove_button(self, city_frame):
        index = self.city_frames.index(city_frame)
        if index == 0: return
        
        button = self.remove_buttons[index - 1]
        if button.winfo_exists():  # Check if the widget still exists
            button.configure(state="disabled")
            
    def enable_remove_button(self, city_frame):
        index = self.city_frames.index(city_frame)
        if index == 0: return
        
        button = self.remove_buttons[index - 1]
        if button.winfo_exists():  # Check if the widget still exists
            button.configure(state="normal")
    
    def apply_decorations(self, label):
        self.apply_color(label)
    
    def apply_color(self, label):
        label.configure(fg="#333333")  # Apply a dark color for text for better readability

    def apply_font(self, widget):
        widget.configure(font=("Helvetica", 14), fg="#333333")  # Apply font and text color
        
    def apply_font(self, widget):
        """Applies the general font style."""
        widget.configure(font=("Helvetica", 12))
        
    def apply_border(self, widget):
        widget.configure(bd=2, relief="solid", width=20)  # Add border to input field

    def apply_border(self, entry_widget):
        """Applies border style to the entry widget."""
        entry_widget.configure(bd=2, relief="solid")
        
    def apply_button_style(self, button):
        button.configure(font=("Helvetica", 12, "bold"), relief="raised", height=1, width=12)
        button.configure(activebackground="#357ABD", activeforeground="white")

    def apply_button_style(self, button):
        """Applies consistent style to all buttons."""
        button.configure(width=20)

