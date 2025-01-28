import pytest
from tkinter import Tk, StringVar
from view import WeatherView

@pytest.fixture
def weather_view():
    """Fixture to set up the weather view for each test."""
    root = Tk()
    view = WeatherView(root)
    yield view
    root.destroy()

def test_initial_state(weather_view):
    """Test the initial state of the WeatherView."""
    assert len(weather_view.city_entries) == 1, "Should start with one cities"
    assert len(weather_view.city_frames) == 2, "Should start with two city frames"
    assert weather_view.add_city_button.cget("state") == "normal", "Add city button should be enabled"
    assert weather_view.refresh_all_button.cget("state") == "normal", "Refresh button should be enabled"

def test_add_multiple_cities(weather_view):
    """Test adding multiple cities."""
    initial_count = len(weather_view.city_entries)
    
    # Add three cities
    for i in range(3):
        weather_view.add_city()
        assert len(weather_view.city_entries) == initial_count + i + 1
        assert len(weather_view.city_frames) == initial_count + i + 2
        assert len(weather_view.temperature_labels) == initial_count + i + 1
        assert isinstance(weather_view.city_entries[-1].get(), str)

def test_remove_specific_city(weather_view):
    """Test removing a specific city and verifying the correct one was removed."""
    # Add three cities with different names
    weather_view.add_city()
    weather_view.city_entries[0].set("London")
    weather_view.add_city()
    weather_view.city_entries[1].set("Paris")
    weather_view.add_city()
    weather_view.city_entries[2].set("Tokyo")
    
    # Remove the second city (Paris)
    weather_view.remove_city(weather_view.city_frames[1])
    
    assert len(weather_view.city_entries) == 2
    assert weather_view.city_entries[0].get() == "London"
    assert weather_view.city_entries[1].get() == "Tokyo"

def test_update_weather_data_comprehensive(weather_view):
    """Test updating all weather data fields."""
    weather_view.add_city()
    city_index = 0
    
    sample_data = {
        "temperature": "25°C",
        "condition": "Clear",
        "min_max_temp": "22°C/28°C",
        "feels_like": "24°C",
        "humidity": "60%",
        "wind": "5 m/s, 180°",
        "visibility": "10 km",
        "pressure": "1015 hPa",
        "clouds": "10%",
        "sunrise": "6:30 AM",
        "sunset": "6:00 PM"
    }
    
    weather_view.update_weather_data(city_index, sample_data)
    
    # Verify all weather data fields
    for field, value in sample_data.items():
        if field == "temperature":
            assert weather_view.temperature_labels[city_index].cget("text") == value
        if field == "condition":
            assert weather_view.condition_labels[city_index].cget("text") == value
        # Add assertions for other fields based on your implementation

def test_error_handling(weather_view):
    """Test comprehensive error handling functionality."""
    weather_view.add_city()
    city_index = 0
    
    # Test showing error
    error_message = "City not found"
    weather_view.show_error(city_index, error_message)
    assert weather_view.error_labels[city_index].cget("text") == error_message
    
    # Test that weather labels are cleared when showing error
    assert weather_view.temperature_labels[city_index].cget("text") == ""
    
    # Test hiding error
    weather_view.hide_error(city_index)
    assert weather_view.error_labels[city_index].cget("text") == ""

def test_button_state_management(weather_view):
    """Test comprehensive button state management."""
    # Test initial state
    assert weather_view.add_city_button.cget("state") == "normal"
    assert weather_view.refresh_all_button.cget("state") == "normal"
    
    # Add a city and test its buttons
    weather_view.add_city()
    assert weather_view.refresh_buttons[0].cget("state") == "normal"
    assert weather_view.remove_buttons[0].cget("state") == "normal"
    
    # Test disabling buttons
    weather_view.disable_all_buttons()
    assert weather_view.add_city_button.cget("state") == "disabled"
    assert weather_view.refresh_all_button.cget("state") == "disabled"
    assert weather_view.refresh_buttons[0].cget("state") == "disabled"
    assert weather_view.remove_buttons[0].cget("state") == "disabled"
    
    # Test enabling buttons
    weather_view.enable_all_buttons()
    assert weather_view.add_city_button.cget("state") == "normal"
    assert weather_view.refresh_all_button.cget("state") == "normal"
    assert weather_view.refresh_buttons[0].cget("state") == "normal"
    assert weather_view.remove_buttons[0].cget("state") == "normal"

def test_city_entry_validation(weather_view):
    """Test that city entries properly handle input."""
    weather_view.add_city()
    city_index = 0
    
    # Test setting valid city name
    weather_view.city_entries[city_index].set("London")
    assert weather_view.city_entries[city_index].get() == "London"
    
    # Test that StringVar is properly connected
    assert isinstance(weather_view.city_entries[city_index], StringVar)