import requests
import re
from geopy.geocoders import Nominatim

API_KEY = "ca689f67c64585a94fe0e714329790f6"

# Weather class to manage weather info
class Weather:
    def __init__(self, city_name):
        # Constructor to initialize city name
        self.city_name = city_name

    def check_weather(self):
        # Method to get info from OpenWeather API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Parsing JSON response
            return self.parse_weather_data(data)
        else:
            # Returning none if weather cannot be fetched
            return None

    @staticmethod
    def parse_weather_data(data):
        # Static method to extract relevant weather info from JSON
        if not data:
            return None
        weather_info = data.get("weather", [{}])[0]
        temperature_celsius = data.get("main", {}).get("temp", 0)
        temperature_fahrenheit = Weather.celsius_to_fahrenheit(temperature_celsius)
        return {
            "main": weather_info.get("main", ""),
            "description": weather_info.get("description", ""),
            "temperature_celsius": temperature_celsius,
            "temperature_fahrenheit": temperature_fahrenheit,
        }

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        # Static method to convert celsius in fahrenheit
        return round((celsius * 9/5) + 32, 1)

    def display_weather_information(self, weather_data):
        # Method to display weather info
        temperature_celsius = int(weather_data["temperature_celsius"])
        temperature_fahrenheit = weather_data["temperature_fahrenheit"]
        print(f"------ Weather information for {self.city_name} -------")
        print(f"- Main: {weather_data['main']}")
        print(f"- Description: {weather_data['description']}")
        print(f"- Temperature: {temperature_celsius}°C / {temperature_fahrenheit}°F\n")


def parse_distance_input(distance_input):
    # Function to parse the input for distance provided by user
    match = re.match(r"(\d+(\.\d+)?)\s*(km|kilometers|ml|miles)?", distance_input, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(3)
        if unit and unit.lower() in ["km", "kilometers"]:
            return value, "metric"
        elif unit and unit.lower() in ["ml", "miles"]:
            return value, "american"
    raise ValueError("Invalid distance format. Add km/kilometres or ml/miles to distance (e.g. 300 km/400 miles).")


def calculate_fuel_needed(distance, fuel_consumption, unit_system):
    # Function to calculate fuel needed for the journey
    if unit_system == "metric":
        return (fuel_consumption / 100) * distance
    elif unit_system == "american":
        return distance / fuel_consumption
    raise ValueError("Invalid unit system")


def main():
    # Main function to control program flow
    geolocator = Nominatim(user_agent="my_app")
    city_name = None
    while True:
        try:
            if not city_name:
                # Ask user for destination city
                city_name = input("Enter your destination city: ")
                location = geolocator.geocode(city_name)
                if not location:
                    print("Sorry, the city could not be found. Try again.")
                    # Reset city_name if invalid
                    city_name = None
                    continue

            distance = None
            # Loop until valid distance is entered
            while distance is None:
                # Ask user for the distance input
                distance_input = input("Enter the distance of the journey (in km or miles): ")
                try:
                    distance, unit_system = parse_distance_input(distance_input)
                    if distance < 0:
                        raise ValueError("Distance cannot be negative.")
                except ValueError as ve:
                    # Print error message
                    print(ve)
                    # Ask for distance input again
                    continue

            fuel_consumption = None
            while fuel_consumption is None or fuel_consumption <=0:
                try:
                    # Ask user for car consumption
                    fuel_consumption = float(input("Enter car's fuel consumption (in liters per 100 km or miles per gallon): "))
                    if fuel_consumption <= 0:
                        raise ValueError("Car fuel consumption must be positive.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

            fuel_price = None
            while fuel_price is None or fuel_price <= 0:
                try:
                    # Ask user for fuel price
                    fuel_price = float(input(f"Enter the price of fuel (per liter or gallon): "))
                    if fuel_price <= 0:
                        raise ValueError("Fuel price must be positive.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

            # Calculating fuel needed for the journey
            fuel_needed = calculate_fuel_needed(distance, fuel_consumption, unit_system)
            total_fuel_cost = fuel_needed * fuel_price
            print(f"\nFuel needed for the journey: {fuel_needed:.2f} gallons" if unit_system ==
                  "american" else f"\nFuel needed for the journey: {fuel_needed:.2f} liters")
            print(f"Total estimated fuel cost: {total_fuel_cost:.2f}")

            # Using geopy to display coordinates of city
            location = geolocator.geocode(city_name)
            if location:
                print(f"Coordinates of {city_name}: Latitude: {location.latitude:.2f}, Longitude: {location.longitude:.2f}\n")

                weather_obj = Weather(city_name)
                weather_data = weather_obj.check_weather()
                if weather_data:
                    weather_obj.display_weather_information(weather_data)
                    print("Have a safe journey!\n")
                else:
                    print("Error retrieving weather data for the entered city. Please try again.\n")
                    # Reset city name if weather data retrieval fails
                    city_name = None
                    continue

        except ValueError as e:
            print(str(e))
            continue

        else:
            break


if __name__ == "__main__":
    main()
