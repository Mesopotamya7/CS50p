from project import Weather, parse_distance_input, calculate_fuel_needed
import pytest


class TestWeather:
    def test_check_weather(self, monkeypatch):
        def mock_input(_): return "New York"
        monkeypatch.setattr("builtins.input", mock_input)

        weather_obj = Weather("New York")
        weather_data = weather_obj.check_weather()

        assert weather_data is not None
        assert isinstance(weather_data, dict)
        assert "main" in weather_data
        assert "description" in weather_data
        assert "temperature_celsius" in weather_data
        assert "temperature_fahrenheit" in weather_data

    def test_parse_distance_input(self):
        distance, unit_system = parse_distance_input("300 km")
        assert distance == 300
        assert unit_system == "metric"

        distance, unit_system = parse_distance_input("400 miles")
        assert distance == 400
        assert unit_system == "american"

    def test_calculate_fuel_needed(self):
        fuel_needed = calculate_fuel_needed(300, 7.2, "metric")
        assert abs(fuel_needed - 21.6) < 0.01

        fuel_needed = calculate_fuel_needed(400, 25, "american")
        assert abs(fuel_needed - 16) < 0.01

    def test_invalid_distance_input(self):
        with pytest.raises(ValueError) as e:
            parse_distance_input("300")
        assert str(e.value) == "Invalid distance format. Add km/kilometres or ml/miles to distance (e.g. 300 km/400 miles)."

    def test_invalid_unit_system(self):
        with pytest.raises(ValueError) as e:
            calculate_fuel_needed(300, 7.2, "invalid_unit")
        assert str(e.value) == "Invalid unit system"
