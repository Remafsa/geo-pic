import requests
import json
from datetime import datetime

# Your Google API Key
API_KEY = 'AIzaSyDZBKRccjcRs2ke8ERqv6tDg3joFaBg33c'

def get_place_details(place_names):
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    photo_base_url = "https://maps.googleapis.com/maps/api/place/photo"
    results = []

    for place in place_names:
        # Fetch place_id, geometry, and google_id from the Find Place API
        params = {
            'input': place,
            'inputtype': 'textquery',
            'fields': 'place_id,geometry',
            'key': API_KEY
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['candidates']:
            place_data = data['candidates'][0]
            place_id = place_data['place_id']
            lat_lng = place_data['geometry']['location']
            lat = lat_lng['lat']
            lng = lat_lng['lng']

            # Get place details (including photos) using the Place Details API
            detail_params = {
                'place_id': place_id,
                'fields': 'name,geometry,url,photos',
                'key': API_KEY
            }
            detail_response = requests.get(details_url, params=detail_params)
            detail_data = detail_response.json()

            if 'result' in detail_data:
                place_result = detail_data['result']
                name = place_result.get('name', '')
                google_id = f"{lat},{lng}"
                location_link = place_result.get('url', '')

                # Get up to 15 photos
                photo_references = get_photo_references(place_result)
                for idx, photo_data in enumerate(photo_references):
                    photo_reference = photo_data.get('photo_reference')
                    photo_url = f"{photo_base_url}?photoreference={photo_reference}&maxwidth=400&key={API_KEY}"
                    photo_url_big = f"{photo_base_url}?photoreference={photo_reference}&maxwidth=2048&key={API_KEY}"
                    photo_date = convert_timestamp_to_date(photo_data.get('time', ''))
                    photo_upload_source = photo_data.get('html_attributions', None)

                    # Append each photo as a separate entry
                    results.append({
                        "query": place,
                        "name": name,
                        "google_id": google_id,
                        "place_id": place_id,
                        "location_link": location_link,
                        "photo_id": photo_reference,
                        "photo_url": photo_url,
                        "photo_url_big": photo_url_big,
                        "latitude": lat,
                        "longitude": lng,
                        "photo_date": photo_date,
                        "photo_upload_source": photo_upload_source,
                        "photo_source_video": None,
                        "photo_tags": None,
                        "photo_tag_ids": None,
                        "original_photo_url": photo_url_big
                    })
        else:
            # Handle case where no data is found
            results.append({
                "query": place,
                "name": None,
                "google_id": None,
                "place_id": None,
                "location_link": None,
                "photo_id": None,
                "photo_url": None,
                "photo_url_big": None,
                "latitude": None,
                "longitude": None,
                "photo_date": None,
                "photo_upload_source": None,
                "photo_source_video": None,
                "photo_tags": None,
                "photo_tag_ids": None,
                "original_photo_url": None
            })

    return results

def get_photo_references(place_result):
    """Get up to 15 photo references for a place."""
    if 'photos' in place_result:
        # Return the photo details including the timestamp
        return [{'photo_reference': photo['photo_reference'], 'time': photo.get('time', None)} for photo in place_result['photos'][:15]]
    return []

def convert_timestamp_to_date(timestamp):
    """Convert timestamp to a readable date format."""
    if timestamp:
        return datetime.utcfromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')
    return None

def save_results_to_json(data, filename='place_details.json'):
    """Save the results to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
