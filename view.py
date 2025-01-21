import tkinter as tk

class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")

        # City Selection
        self.city_label = tk.Label(root, text="Select City:")
        self.city_label.pack()

        self.city_menu = tk.StringVar(root)
        self.city_menu.set("London")  # Default selection
        self.city_dropdown = tk.OptionMenu(root, self.city_menu, "London", "Paris", "New York")
        self.city_dropdown.pack()

        # Display Weather Data
        self.temperature_label = tk.Label(root, text="Temperature: --°C")
        self.temperature_label.pack()

        self.condition_label = tk.Label(root, text="Condition: --")
        self.condition_label.pack()

        # Refresh Button
        self.refresh_button = tk.Button(root, text="Refresh")
        self.refresh_button.pack()

    def update_temperature(self, text):
        self.temperature_label.config(text=text)
        self.apply_decorations(self.temperature_label)

    def update_condition(self, text):
        self.condition_label.config(text=text)

    def apply_decorations(self, label):
        self.apply_color(label)

    # Decorators for the label 
    def apply_color(self, label):
        label.config(fg="blue")