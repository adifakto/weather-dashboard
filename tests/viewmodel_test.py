import pytest
from unittest.mock import MagicMock
from viewmodel import WeatherViewModel
from view import WeatherView

@pytest.fixture
def weather_view_model():
    """Fixture to set up the WeatherViewModel instance with mocked dependencies."""
    mock_model = MagicMock()
    mock_view = MagicMock()
    view_model = WeatherViewModel(mock_model, mock_view)
    return view_model, mock_model, mock_view

def test_on_new_city_added(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    city_index = 2
    view_model.on_new_city_added(city_index)
    
    # Check if configure_refresh_button was called with the correct index
    mock_view.configure_refresh_button.assert_called_with(city_index)

def test_configure_refresh_button(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    idx = 0
    view_model.configure_refresh_button(idx)
    
    # Check if the correct command is assigned to the button
    mock_view.refresh_buttons[idx].config.assert_called()

def test_add_city_if_not_refreshing(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    
    # Case when not refreshing
    view_model.is_refreshing = False
    view_model.add_city_if_not_refreshing()
    mock_view.add_city.assert_called_once()

    # Case when refreshing
    view_model.is_refreshing = True
    view_model.add_city_if_not_refreshing()
    mock_view.add_city.assert_not_called()

def test_update_weather(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    city_index = 0
    mock_data = {
        'temperature': 22,
        'weather_condition': 'Sunny',
        'min_tempreture': 18,
        'max_tempreture': 26,
        'feels_like': 21,
        'humidity': 60,
        'wind_speed': 5,
        'wind_degree': 180,
        'visibility': 10000,
        'pressure': 1013,
        'clouds': 10,
        'sunrise': 1632456933,
        'sunset': 1632500853
    }

    mock_model.fetch_weather.return_value = mock_data
    view_model.update_weather(city_index)
    
    # Check if the correct methods are called with the expected data
    mock_view.update_temperature.assert_called_with(city_index, "Temperature: 22°C")
    mock_view.update_condition.assert_called_with(city_index, "Condition: Sunny")
    mock_view.update_min_max_tempreture.assert_called_with(city_index, "18°C/26°C")
    mock_view.update_feels_like.assert_called_with(city_index, "Feels Like: 21°C")

def test_update_weather_all(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    view_model.is_refreshing = False
    view_model.update_weather_all()

    # Check if the background thread has started (Mocking Thread target function)
    mock_model.fetch_weather.assert_called()
    mock_view.disable_all_buttons.assert_called_once()
    mock_view.enable_all_buttons.assert_called_once()

def test_fetch_weather_data_error_handling(weather_view_model):
    view_model, mock_model, mock_view = weather_view_model
    mock_model.fetch_weather.side_effect = Exception("API error")
    view_model.update_weather_all()
    
    # Check if the error message is properly shown on the UI
    mock_view.show_error.assert_called()
