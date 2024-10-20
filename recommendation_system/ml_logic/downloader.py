import os
import requests
import json
import pandas as pd
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
import os
import pandas as pd
import requests
import os
import pandas as pd
import requests

def download_images_from_file(file_path, file_type='csv', url_column='photo_url', name_column='name', save_folder='', save_csv=False, csv_file_name='output.csv'):
    """
    Download images from a file and save them locally in a specified folder.

    Parameters:
    - file_path: str, path to the input file (CSV or JSON).
    - file_type: str, type of the input file ('csv' or 'json').
    - url_column: str, name of the column containing the image URLs (default is 'photo_url').
    - name_column: str, name of the column for naming images (default is 'name').
    - save_folder: str, folder where the images will be saved (default is 'geoclip/Images').
    - save_csv: bool, whether to save the updated DataFrame as a CSV file (default is False).
    - csv_file_name: str, name of the CSV file to save the DataFrame (default is 'output.csv').

    Returns:
    - df: The updated DataFrame with the 'IMG_FILE' column.
    """
    # Load the DataFrame from the specified file
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'json':
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'json'.")

    # Create a folder to save images if it doesn't already exist
    os.makedirs(save_folder, exist_ok=True)
    print(f"Images will be saved in: {save_folder}")

    # Dictionary to count occurrences of names
    counter = {}

    # Iterate through the DataFrame row by row
    for index, row in df.iterrows():
        # Extract the image URL and restaurant name from the current row
        image_url = row[url_column]
        name = row[name_column]

        # Initialize or increment the counter for the restaurant name
        if name not in counter:
            counter[name] = 0
        counter[name] += 1

        # Create a unique image name using the restaurant name and the counter
        image_name = os.path.join(save_folder, f"{name}_{counter[name]}.jpg")

        try:
            # Send a GET request to the image URL with a timeout of 10 seconds
            response = requests.get(image_url, timeout=10)

            # Check if the response indicates success (status code 200)
            if response.status_code == 200:
                # Save the image content to the specified file
                with open(image_name, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {image_name}")

                # Update the 'IMG_FILE' column in the DataFrame with the saved image path
                df.at[index, 'IMG_FILE'] = image_name
            elif response.status_code == 400:
                # Handle bad request errors
                print(f"Skipping image from {image_url} (status code: {response.status_code})")
            else:
                # Handle other unsuccessful status codes
                print(f"Failed to download image from {image_url} (status code: {response.status_code})")
        except Exception as e:
            # Handle any exceptions that occur during the request
            print(f"Error downloading image from {image_url}: {e}")

    # If saving the updated DataFrame as a CSV file is desired, do that
    if save_csv:
        df.to_csv(csv_file_name, index=False)
        print(f"DataFrame saved to {csv_file_name}")

    return df
