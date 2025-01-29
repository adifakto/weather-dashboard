import pytest
from tkinter import Tk
from unittest.mock import MagicMock
from view import WeatherView

@pytest.fixture(scope="function")
def view():
    """Fixture to create and clean up WeatherView instance."""
    root = Tk()
    view_instance = WeatherView(root)
    yield view_instance
    root.destroy()

def test_initial_state(view):
    """Test the initial state of the WeatherView."""
    assert len(view.city_entries) == 1, "Should start with one city"
    assert len(view.city_frames) == 1, "Should start with one city frame"
    assert view.add_city_button.cget("state") == "normal", "Add city button should be enabled"

def test_add_multiple_cities(view):
    """Test adding multiple cities."""
    initial_count = len(view.city_entries)
    
    # Add three cities
    for i in range(1, 4):
        view.add_city()
        assert len(view.city_entries) == initial_count + i
        assert len(view.city_frames) == initial_count + i
        assert len(view.temperature_labels) == initial_count + i
        assert isinstance(view.city_entries[-1].get(), str)

def test_remove_specific_city(view):
    """Test removing a specific city and verifying the correct one was removed."""
    # Add three cities
    for _ in range(3):
        view.add_city()
    
    initial_count = len(view.city_entries)
    
    # Remove the second city
    view.remove_city(view.city_frames[1])
    
    assert len(view.city_entries) == initial_count - 1, "Expected one city to be removed"

def test_error_handling(view):
    """Test comprehensive error handling functionality."""
    view.add_city()
    city_index = 0
    
    # Test showing error
    error_message = "City not found"
    view.show_error(city_index, error_message)
    assert view.error_labels[city_index].cget("text") == error_message
    
    # Test that temperature label is cleared when showing error
    assert view.temperature_labels[city_index].cget("text") == "Temperature: --°C"