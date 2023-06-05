# Imports
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Global Variables
# API Key
API_KEY = os.getenv("API_KEY")
# API URL
API_URL = "http://api.aviationstack.com/v1/flights"
# Parameters
PARAMS = {
    "access_key": API_KEY,
    "dep_iata": "EZE",
    "airline_name": "British Airways",
    "flight_iata": "BA244"
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
    for flight in data["data"]:
        if flight["flight_date"] == "2023-06-05": # The date of the flight we want to track
            return flight



# Testing
flight_data = get_flight_data()
print(flight_data)
