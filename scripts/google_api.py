import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv('API_KEY')

if api_key is None:
    raise ValueError("API_KEY not found. Please check your .env file.")


def get_place_id(api_key, restaurant_name, area=""):
    """
    Get the PLACE_ID of a restaurant using its name and an optional area.

    :param restaurant_name: The name of the restaurant.
    :param area: An optional string representing the area (e.g., city name).
    :return: The PLACE_ID of the restaurant if found, else None.
    """
    query = f"{restaurant_name} {area}".strip()
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

    response = requests.get(search_url)
    results = response.json().get('results', [])

    if results:
        place_id = results[0].get('place_id')
        return place_id
    else:
        return None

def get_place_details(api_key,place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "OK":
            place_details = response.json().get('result', {})
            return place_details
        else:
            print(f"Error: {data.get('status')} - {data.get('error_message', '')}")
    else:
        print(f"Error: Received status code {response.status_code}")
    return {}


def get_nearby_places(api_key, location, radius=1000):
    """
    Get nearby places around a specified location.

    :param location: A string representing the latitude and longitude (e.g., "12.345678,34.567890").
    :param radius: The radius in meters to search for nearby places.
    :return: A list of nearby places.
    """
    nearby_search_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={api_key}"

    response = requests.get(nearby_search_url)
    nearby_places = response.json().get('results', [])

    return nearby_places
