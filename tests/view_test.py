import pytest
from tkinter import Tk, StringVar
from view import WeatherView

# @pytest.fixture
# def weather_view():
#     """Fixture to set up the weather view for each test."""
#     root = Tk()
#     view = WeatherView(root)
#     yield view
#     root.destroy()

def test_initial_state():
    root = Tk()
    view = WeatherView(root)
    yield view
    root.destroy()
    
    """Test the initial state of the WeatherView."""
    assert len(view.city_entries) == 1, "Should start with one cities"
    assert len(view.city_frames) == 1, "Should start with one city frame"
    assert view.add_city_button.cget("state") == "normal", "Add city button should be enabled"
    
def test_add_multiple_cities():
    """Test adding multiple cities."""
    root = Tk()
    view = WeatherView(root)
    yield view
    root.destroy()
    
    initial_count = len(view.city_entries)
    
    # Add three cities
    for i in range(1, 4):
        view.add_city()
        assert len(view.city_entries) == initial_count + i
        assert len(view.city_frames) == initial_count + i
        assert len(view.temperature_labels) == initial_count + i
        assert isinstance(view.city_entries[-1].get(), str)

def test_remove_specific_city():
    """Test removing a specific city and verifying the correct one was removed."""
    root = Tk()
    view = WeatherView(root)
    yield view
    root.destroy()
    
    # Add three cities
    current_cities_counter = len(view.city_entries)
    
    for i in range(1, 4):
        view.add_city()
        current_cities_counter = current_cities_counter + 1
    
    # Remove the second city
    view.remove_city(view.city_frames[1])
    current_cities_counter = current_cities_counter - 1
    
    assert len(view.city_entries) == current_cities_counter # expected 3 cities left

def test_error_handling():
    """Test comprehensive error handling functionality."""
    root = Tk()
    view = WeatherView(root)
    yield view
    root.destroy()
    
    view.add_city()
    city_index = 0
    
    # Test showing error
    error_message = "City not found"
    view.show_error(city_index, error_message)
    assert view.error_labels[city_index].cget("text") == error_message
    
    # Test that weather a label is cleared when showing error
    assert view.temperature_labels[city_index].cget("text") == "Temperature: --°C"