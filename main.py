from model import WeatherModel
from view import WeatherView
from viewmodel import WeatherViewModel

def get_api_key(filename):
    with open(filename, "r") as file:
        return file.read().strip()
    
if __name__ == "__main__":
    API_KEY = get_api_key("key.txt")

    # Initialize components
    model = WeatherModel(API_KEY)
    view = WeatherView()
    view_model = WeatherViewModel(model, view)

    # Run the application
    view.mainloop()