#pip install pillow

import tkinter as tk
from PIL import Image, ImageTk

class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x800")  # Adjust the window size
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

        # Frame for condition label and image
        self.condition_frame = tk.Frame(root, bg="#F1F1F1")
        self.condition_frame.pack(pady=(5, 10))  # Create the frame and add some vertical padding

        # Condition Label inside the frame
        self.condition_label = tk.Label(self.condition_frame, text="Condition: --", font=("Helvetica", 14), bg="#F1F1F1")
        self.condition_label.pack(side="left", padx=(10, 0))  # Align the label to the left side

        # Weather Condition Image (to be placed to the right of the condition label)
        self.condition_image_label = tk.Label(self.condition_frame, bg="#F1F1F1")  # Label to display the condition image
        self.condition_image_label.pack(side="left", padx=(10, 0))  # Place the image to the right of the label

        # Refresh Button
        self.refresh_button = tk.Button(root, text="Refresh", font=("Helvetica", 12), bg="#4A90E2", fg="white")
        self.refresh_button.pack(pady=10)
        self.apply_button_style(self.refresh_button)

        # Weather GIFs (stored as a dictionary for different conditions)
        self.weather_gifs = {
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
        self.current_gif = None  # To keep track of the displayed GIF

    def update_temperature(self, text):
        self.temperature_label.config(text=text)
        self.apply_decorations(self.temperature_label)

    def update_condition(self, text):
        # Extract the condition word by removing "Condition: " if it exists
        condition = text.replace("Condition: ", "").strip()
        print(f"Received condition text: {text}")  # Debug log
        print(f"Extracted condition: {condition}")  # Debug log

        # Update the condition label with the extracted condition
        self.condition_label.config(text=text)

        # Get the GIF path for the condition
        gif_path = self.weather_gifs.get(condition, None)

        if gif_path:
            print(f"GIF path found: {gif_path}")
            self.display_gif(gif_path)
        else:
            print("No matching GIF found.")



    def display_gif(self, gif_path, target_width=70, target_height=70):
        try:
            self.current_gif = Image.open(gif_path)
            self.gif_frames = []

            for frame in range(self.current_gif.n_frames):
                self.current_gif.seek(frame)
                
                # Resize the frame using PIL's resize method
                resized_frame = self.current_gif.copy().resize((target_width, target_height))
                frame_image = ImageTk.PhotoImage(resized_frame)

                # Add the resized frame to the list of frames
                self.gif_frames.append(frame_image)

            self.animate_gif(0)
        except Exception as e:
            self.error_label.config(text=f"Error loading image: {e}")
            self.error_label.pack()

    def animate_gif(self, frame_index):
        """Animate the GIF by cycling through frames."""
        if self.gif_frames:
            frame = self.gif_frames[frame_index]
            self.condition_image_label.config(image=frame)
            self.root.after(100, self.animate_gif, (frame_index + 1) % len(self.gif_frames))

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
