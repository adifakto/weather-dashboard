import tkinter as tk
from model import WeatherModel
from view import WeatherView
from viewmodel import WeatherViewModel

if __name__ == "__main__":
    API_KEY = "5a1c3777d1d06aafd1deae802db9a951"

    root = tk.Tk()

    # Initialize components
    model = WeatherModel(API_KEY)
    view = WeatherView(root)
    view_model = WeatherViewModel(model, view)

    # Run the application
    root.mainloop()