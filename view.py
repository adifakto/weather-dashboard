import tkinter as tk
from tkinter import ttk


class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x500")  # Adjusted size for horizontal scrolling
        self.root.config(bg="#F1F1F1")  # Light grey background for the window

        # Title
        self.title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), fg="#4A90E2")
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
        city_label.grid(row=0, column=0, pady=(10, 5))  # Pack with padding for better spacing
        self.apply_font(city_label)

        # City Input Field
        city_entry = tk.Entry(city_frame, font=("Helvetica", 14), relief="solid", bd=2, width=20)
        city_entry.insert(0, "London")  # Default text
        city_entry.grid(row=1, column=0, pady=10)  # Pack with padding
        self.apply_border(city_entry)

        # Weather Data Labels
        temperature_label = tk.Label(city_frame, text="Temperature: --°C", font=("Helvetica", 14), bg="#F1F1F1")
        temperature_label.grid(row=2, column=0, pady=(10, 5))  # Pack with padding
        self.apply_font(temperature_label)

        condition_label = tk.Label(city_frame, text="Condition: --", font=("Helvetica", 14), bg="#F1F1F1")
        condition_label.grid(row=3, column=0, pady=(5, 20))  # Pack with padding
        self.apply_font(condition_label)

        # Error Label
        error_label = tk.Label(city_frame, text="", font=("Helvetica", 12), fg="red", bg="#F1F1F1")
        error_label.grid(row=4, column=0, pady=(5, 10))  # Add padding
        error_label.grid_forget()  # Hide by default

        # Add the refresh button above the remove button
        refresh_button = tk.Button(city_frame, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        refresh_button.grid(row=5, column=0, pady=(10, 10))  # Place above the remove button

        # Add the remove button only if this isn't the first city
        if not self.is_first_city:
            remove_button = tk.Button(city_frame, text="Remove", font=("Helvetica", 12), bg="#FF4C4C", fg="white",
                                      command=lambda: self.remove_city(city_frame))
            remove_button.grid(row=6, column=0, pady=(10, 10))  # Pack the remove button

        # Mark the first city as added
        self.is_first_city = False

        # Append to the lists
        self.city_entries.append(city_entry)
        self.temperature_labels.append(temperature_label)
        self.condition_labels.append(condition_label)
        self.error_labels.append(error_label)
        self.city_frames.append(city_frame)  # Add the city frame to the list

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
            self.temperature_labels.pop(index)
            self.condition_labels.pop(index)
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

    def update_temperature(self, city_index, text):
        """Update the temperature label for the city at city_index."""
        self.temperature_labels[city_index].config(text=text)
        self.apply_decorations(self.temperature_labels[city_index])

    def update_condition(self, city_index, text):
        """Update the condition label for the city at city_index."""
        self.condition_labels[city_index].config(text=text)

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