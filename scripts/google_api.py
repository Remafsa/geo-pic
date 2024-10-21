import requests


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

def get_place_details(self, place_id):
    """
    Get details of a place using its PLACE_ID.

    :param place_id: The PLACE_ID of the place.
    :return: Details of the place as a dictionary.
    """
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={self.api_key}"

    response = requests.get(details_url)
    place_details = response.json().get('result', {})

    return place_details

def get_nearby_places(self, location, radius=1000):
    """
    Get nearby places around a specified location.

    :param location: A string representing the latitude and longitude (e.g., "12.345678,34.567890").
    :param radius: The radius in meters to search for nearby places.
    :return: A list of nearby places.
    """
    nearby_search_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={self.api_key}"

    response = requests.get(nearby_search_url)
    nearby_places = response.json().get('results', [])

    return nearby_places


def extract_reviews(place_details):
    """
    Extracts all review texts from the place details.

    :param place_details: A dictionary containing details about the place, including reviews.
    :return: A list of review texts.
    """
    all_reviews = []
    reviews = place_details.get('reviews', [])

    for review in reviews:
        review_text = review.get('text', 'No review text available')
        all_reviews.append(review_text)

    return all_reviews

# def main():
#     # Replace with your Google Places API key
#     API_KEY = "YOUR_API_KEY"

#     restaurant_name = "Restaurant Name"
#     area = "Riyadh"  # Specify the area or city if known

#     # Step 1: Get PLACE_ID
#     place_id = get_place_id(API_KEY, restaurant_name, area)

#     if place_id:
#         print(f"PLACE_ID: {place_id}")

#         # Step 2: Get place details
#         place_details = get_place_details(API_KEY, place_id)
#         print("Place Details:", place_details)

#         # If you want to find nearby places, you need the location coordinates of the restaurant
#         if 'geometry' in place_details:
#             location = f"{place_details['geometry']['location']['lat']},{place_details['geometry']['location']['lng']}"
#             # Step 3: Get nearby places
#             nearby_places = get_nearby_places(API_KEY, location)
#             print("Nearby Places:")
#             for place in nearby_places:
#                 print(f"- {place.get('name')} (Rating: {place.get('rating')}, Address: {place.get('vicinity')})")
#     else:
#         print("Restaurant not found.")

# if __name__ == "__main__":
#     main()
