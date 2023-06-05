# Imports
import requests
from dotenv import load_dotenv
import os
import folium
import datetime

load_dotenv()

# Global Variables
# API Key
API_KEY = os.getenv("API_KEY")
# API URL
API_URL = "http://api.aviationstack.com/v1/flights"
# FLIGHT LABS
FL_API_KEY = os.getenv("FLIGHTLAB_API_KEY")
# FLIGHT LABS API URL
FL_API_URL = "https://airlabs.co/api/v9/flights"
# EZE Coordinates
EZE_LAT = -34.814782053586775
EZE_LON = -58.54361745304692

AIRLINE = os.getenv("AIRLINE_NAME")
FL_IATA = os.getenv("FLIGHT_IATA")
# Parameters
PARAMS = {
    "access_key": API_KEY,
    "dep_iata": "EZE",
    "airline_name": AIRLINE,
    "flight_iata": FL_IATA,
}

FL_PARAMS = {
    "api_key": FL_API_KEY,
    "flight_iata": FL_IATA
}


# Functions
def get_flight_data() -> dict:
    """Gets flight data from API"""
    # Make API call
    response = requests.get(API_URL, params=PARAMS, json=True)
    response.raise_for_status()
    # Convert response to JSON
    data = response.json()
    # Return data
    try:
        for flight in data["data"]:
            if flight["flight_date"] == "2023-06-05":  # The date of the flight we want to track
                return flight
    except IndexError:
        return {"Flight": "No flight found."}


def get_flight_location() -> dict:
    """Gets flight location from API"""
    # Make API call
    response = requests.get(FL_API_URL, params=FL_PARAMS)
    response.raise_for_status()
    # Convert response to JSON
    data = response.json()
    # Return data
    try:
        return data
    except IndexError:
        return {"Flight": "No flight found."}


def create_map(latitude: float, longitude: float) -> None:
    """Creates map"""
    # Create map
    map = folium.Map(location=[latitude, longitude], zoom_start=10)
    # Add marker
    folium.Marker(
        location=[latitude, longitude],
        popup="EZE",
        icon=folium.Icon(color="red", icon="plane"),
    ).add_to(map)
    # Save map
    map.save("flight_map.html")


def print_link_to_map() -> None:
    """Prints link to map"""
    path = os.path.abspath("flight_map.html")
    rel_path = "flight_map.html"
    print("Map created. Click on the link to view it.")
    print(f"file://{path}")
    print(f"file://{rel_path}")


def print_flight_info(data: dict) -> None:
    """Prints flight info"""
    departure_time = datetime.datetime.strptime("2023-06-05T17:40:00", "%Y-%m-%dT%H:%M:%S")
    arrival_time = datetime.datetime.fromisoformat(data["arrival"]["scheduled"])
    time_now = datetime.datetime.now()

    print(f"Flight: {data['flight']['iata']}")
    print(f"Airline: {data['airline']['name']}")
    print(f"Departure: {data['departure']['airport']}")
    print(f"Arrival: {data['arrival']['airport']}")
    print(f"Departure Time: {departure_time}")
    print(f"Arrival Time: {arrival_time}")
    print(f"Total Time In Air: {arrival_time - departure_time}")


# Testing
flight_data = get_flight_data()
print_flight_info(flight_data)

flight_location = get_flight_location()
map_lat = flight_location["response"][0]["lat"]
map_lon = flight_location["response"][0]["lng"]
create_map(map_lat, map_lon)

print_link_to_map()
