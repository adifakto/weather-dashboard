import tkinter as tk

class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("400x350")  # Adjust the window size
        self.root.config(bg="#F1F1F1")  # Light grey background for the window

        # Title
        self.title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), fg="#4A90E2")
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

        # Weather Data Labels
        self.temperature_label = tk.Label(root, text="Temperature: --°C", font=("Helvetica", 14), bg="#F1F1F1")
        self.temperature_label.pack(pady=(10, 5))
        self.apply_font(self.temperature_label)
        
        self.condition_label = tk.Label(root, text="Condition: --", font=("Helvetica", 14), bg="#F1F1F1")
        self.condition_label.pack(pady=(5, 20))
        self.apply_font(self.condition_label)

        # Refresh Button
        self.refresh_button = tk.Button(root, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        self.refresh_button.pack(pady=10)
        self.apply_button_style(self.refresh_button)

    def update_temperature(self, text):
        self.temperature_label.config(text=text)
        self.apply_decorations(self.temperature_label)

    def update_condition(self, text):
        self.condition_label.config(text=text)

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
