import tkinter as tk
from tkinter import ttk

class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x500")
        self.root.config(bg="#F1F1F1")

        # Title
        self.title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), fg="#4A90E2")
        self.title_label.pack(pady=20)

        # Scrollable area
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(pady=(10, 0), padx=20, fill="both", expand=True)

        # Canvas for horizontal scrolling
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame to hold city entries and weather data
        self.city_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.city_frame, anchor="nw")

        # Lists to hold dynamic widgets
        self.city_entries = []
        self.temperature_labels = []
        self.condition_labels = []
        self.error_labels = []
        self.remove_buttons = []
        self.city_frames = []

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x", pady=(10, 20))
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Add initial city
        self.add_city()

        # Button frame
        self.button_frame = tk.Frame(root, bg="#F1F1F1")
        self.button_frame.pack(pady=10, fill="x")

        # Add City Button
        self.add_city_button = tk.Button(self.button_frame, text="Add City", font=("Helvetica", 12), bg="#4A90E2",
                                         fg="white", command=self.add_city)
        self.add_city_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew", ipadx=8, ipady=4)

        # Refresh Button
        self.refresh_button = tk.Button(self.button_frame, text="Refresh All", font=("Helvetica", 12), bg="#4A90E2",
                                        fg="white")
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew", ipadx=8, ipady=4)

        # Configure button frame
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def add_city(self):
        """Adds a new city entry, temperature, condition, and refresh button."""
        city_frame = tk.Frame(self.city_frame, bd=2, relief="solid", padx=10, pady=5)
        row, column = 0, len(self.city_entries)
        city_frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")

        # City Input Label
        city_label = tk.Label(city_frame, text="Enter City:", font=("Helvetica", 12), bg="#F1F1F1")
        city_label.grid(row=0, column=0, pady=(10, 5))

        # City Input Field
        city_entry = tk.Entry(city_frame, font=("Helvetica", 14), relief="solid", bd=2, width=20)
        city_entry.insert(0, "London")
        city_entry.grid(row=1, column=0, pady=10)

        # Weather Data Labels
        temperature_label = tk.Label(city_frame, text="Temperature: --°C", font=("Helvetica", 14), bg="#F1F1F1")
        temperature_label.grid(row=2, column=0, pady=(10, 5))

        condition_label = tk.Label(city_frame, text="Condition: --", font=("Helvetica", 14), bg="#F1F1F1")
        condition_label.grid(row=3, column=0, pady=(5, 20))

        # Error Label
        error_label = tk.Label(city_frame, text="", font=("Helvetica", 12), fg="red", bg="#F1F1F1")
        error_label.grid(row=4, column=0, pady=(5, 10))
        error_label.grid_forget()

        # Refresh Button
        refresh_button = tk.Button(city_frame, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        refresh_button.grid(row=5, column=0, pady=(10, 10))

        # Remove Button (only add if it's not the first city)
        if len(self.city_entries) > 0:  # Only add the remove button if it's not the first city
            remove_button = tk.Button(city_frame, text="Remove", font=("Helvetica", 12), bg="#FF4C4C", fg="white",
                                      command=lambda frame=city_frame: self.remove_city(frame))
            remove_button.grid(row=6, column=0, pady=(10, 10))
            self.remove_buttons.append(remove_button)

        # Append to lists
        self.city_entries.append(city_entry)
        self.temperature_labels.append(temperature_label)
        self.condition_labels.append(condition_label)
        self.error_labels.append(error_label)
        self.city_frames.append(city_frame)

        # Update scroll region
        self.update_scroll_region()

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
            self.temperature_labels.pop(index)
            self.condition_labels.pop(index)
            self.error_labels.pop(index)

            # Only remove the remove button if it exists
            if index < len(self.remove_buttons):
                self.remove_buttons.pop(index)

            # Shift remaining cities
            for i in range(index, len(self.city_entries)):
                self.city_frames[i].grid_forget()
                self.city_frames[i].grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

            # Update the scroll region
            self.update_scroll_region()
        except ValueError:
            print("City frame not found in the list.")

    def update_scroll_region(self):
        """Updates the scroll region and adjusts the scrollbar visibility."""
        self.city_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        if self.canvas.bbox("all")[2] <= self.canvas.winfo_width():
            self.scrollbar.pack_forget()
        else:
            if not self.scrollbar.winfo_ismapped():
                self.scrollbar.pack(side="bottom", fill="x", pady=(10, 20))

    def update_temperature(self, city_index, text):
        """Update the temperature label for the city at city_index."""
        self.temperature_labels[city_index].config(text=text)

    def update_condition(self, city_index, text):
        """Update the condition label for the city at city_index."""
        self.condition_labels[city_index].config(text=text)

    def show_error(self, city_index, error_message):
        """Displays error message for the city at city_index."""
        self.error_labels[city_index].config(text=error_message)
        self.error_labels[city_index].grid(row=4, column=0)

    def hide_error(self, city_index):
        """Hides the error message for the city at city_index."""
        self.error_labels[city_index].grid_forget()

    def get_city_name(self, city_index):
        """Returns the city name from the entry field."""
        return self.city_entries[city_index].get()

    def disable_all_buttons(self):
        """Disables all buttons in the UI."""
        self.add_city_button.config(state="disabled")
        self.refresh_button.config(state="disabled")
        for remove_button in self.remove_buttons:
            if remove_button.winfo_exists():  # Check if the button still exists
                remove_button.config(state="disabled")

    def enable_all_buttons(self):
        """Enables all buttons in the UI."""
        self.add_city_button.config(state="normal")
        self.refresh_button.config(state="normal")
        for remove_button in self.remove_buttons:
            if remove_button.winfo_exists():  # Check if the button still exists
                remove_button.config(state="normal")