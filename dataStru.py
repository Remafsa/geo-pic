import json
import requests
import pandas as pd
import os
def json_to_dataframe(file_path):
    """
    Read a JSON file and convert it to a Pandas DataFrame.

    Parameters:
    - file_path: str, path to the JSON file.
    - csv_file_name: str, name of the output CSV file (default is 'output.csv').

    Returns:
    - DataFrame containing the JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print(df.head())


    return df

# Example usage of json_to_dataframe()
#file_path = "/home/mohammed/code/Remafsa/geo-pic/recommendation_system/Outscraper-20241011183106xs96_fine_dining_restaurant.json"
#file_path = ""
#  path up^^^^^^
#df = json_to_dataframe(file_path)

import os
import requests
import pandas as pd

def download_images_from_file(file_path, file_type='csv', url_column='photo_url', name_column='name', lat_column='latitude', lon_column='longitude', save_folder='geoclip/Images', save_csv=False, csv_file_name='output.csv'):
    """
    Download images from a file and save them locally in a specified folder.

    Parameters:
    - file_path: str, path to the input file (CSV or JSON).
    - file_type: str, type of the input file ('csv' or 'json').
    - url_column: str, name of the column containing the image URLs (default is 'photo_url').
    - name_column: str, name of the column for naming images when latitude and longitude are null (default is 'name').
    - lat_column: str, name of the column containing the latitudes (default is 'latitude').
    - lon_column: str, name of the column containing the longitudes (default is 'longitude').
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

    # Dictionary to count occurrences of names and lat/lon combinations
    counter = {'lat_lon': {}, 'name': {}}

    # Iterate through the DataFrame row by row
    for index, row in df.iterrows():
        # Extract the image URL, latitude, and longitude from the current row
        image_url = row[url_column]
        latitude = row[lat_column]
        longitude = row[lon_column]
        name = row[name_column]

        # Determine the naming convention based on latitude and longitude
        if pd.notna(latitude) and pd.notna(longitude):
            # Create a unique key for the latitude and longitude
            location_key = f"{latitude}_{longitude}"
            counter_key = 'lat_lon'
            counter[counter_key][location_key] = counter[counter_key].get(location_key, 0) + 1
            image_name = os.path.join(save_folder, f"{location_key}_{counter[counter_key][location_key]}.jpg")
        else:
            # Use the name column for naming
            name_key = f"{name}"
            counter_key = 'name'
            counter[counter_key][name_key] = counter[counter_key].get(name_key, 0) + 1
            image_name = os.path.join(save_folder, f"{name_key}_{counter[counter_key][name_key]}.jpg")

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
# Example DataFrame setup (replace this with the actual DataFrame)
# Call the function to download images from the DataFrame
#df_p = download_images_from_df(df, save_csv=True, csv_file_name='geo_pic.csv')
# Display the updated DataFrame
#print(df_p)


def save_semi_clean_data(df, lat_column='latitude', lon_column='longitude', IMG_FILE_column='IMG_FILE', output_file='semi_clean_data.csv'):
    """
    Save a DataFrame with only latitude, longitude, and image path to a CSV file in the current directory.

    Parameters:
    - df: DataFrame containing the original data.
    - lat_column: str, name of the column containing latitudes (default is 'latitude').
    - lon_column: str, name of the column containing longitudes (default is 'longitude').
    - IMG_FILE_column: str, name of the column containing image paths (default is 'IMG_FILE').
    - output_file: str, name of the output CSV file (default is 'semi_clean_data.csv').
    """
    # select only the columns interested in
    semi_clean_df = df[[lat_column, lon_column, IMG_FILE_column]]

    # Get the current working directory  to save the file
    current_directory = os.getcwd()

    # Create the full path for the output file with the specified name
    output_path = os.path.join(current_directory, output_file)

    # Save the new DataFrame to a CSV file at the specified location
    semi_clean_df.to_csv(output_path, index=False)
    print(f"Semi-clean data saved to {output_path}")

# Example usage of save_semi_clean_data():
# I have 'geo_pic.csv' as my input file, which will be loaded into a DataFrame
#file_path = "geo_pic.csv"
#file_path = ""
# Load the DataFrame from the CSV file
#df = pd.read_csv(file_path)
# Call the function to save the semi-clean data  just created
#save_semi_clean_data(df_p)
