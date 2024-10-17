import os
import requests
import json
import os
import requests

def download_images(image_urls, downloaded_images_dir="downloaded_images"):
    """
    Downloads images from the provided URLs and saves them to a specified directory.

    Parameters:
    - image_urls (list): List of image URLs to download.
    - downloaded_images_dir (str): Directory to save the downloaded images.

    Returns:
    - local_image_paths (list): List of file paths of downloaded images.
    """
    os.makedirs(downloaded_images_dir, exist_ok=True)  # Create the directory if it doesn't exist
    local_image_paths = []

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                local_image_path = os.path.join(downloaded_images_dir, f"image_{idx}.jpg")
                with open(local_image_path, 'wb') as f:
                    f.write(response.content)
                local_image_paths.append(local_image_path)
                print(f"Successfully downloaded: {local_image_path}")  # Output for successful download
            else:
                print(f"Failed to download {url} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    return local_image_paths
def extract_image_urls_from_json(file_path, downloaded_images_dir="downloaded_images"):
    """
    Reads a JSON file and extracts image URLs.

    Parameters:
    - file_path (str): Path to the JSON file.
    - downloaded_images_dir (str): Directory to store downloaded images (defaults to 'downloaded_images').

    Returns:
    - image_urls (list): List of extracted image URLs.
    """
    # Create directory for downloaded images if it doesn't exist
    os.makedirs(downloaded_images_dir, exist_ok=True)

    # Load data from the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract photo URLs
    image_urls = [item['photo_url'] for item in data if 'photo_url' in item and item['photo_url']]

    return image_urls
