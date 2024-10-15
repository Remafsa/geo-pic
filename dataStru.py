{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import requests\n",
    "import pandas as pd\n",
    "import os\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "def json_to_dataframe(file_path):\n",
    "    \"\"\"\n",
    "    Read a JSON file and convert it to a Pandas DataFrame.\n",
    "\n",
    "    Parameters:\n",
    "    - file_path: str, path to the JSON file.\n",
    "    - csv_file_name: str, name of the output CSV file (default is 'output.csv').\n",
    "\n",
    "    Returns:\n",
    "    - DataFrame containing the JSON data.\n",
    "    \"\"\"\n",
    "    with open(file_path, 'r', encoding='utf-8') as file:\n",
    "        data = json.load(file)\n",
    "\n",
    "    df = pd.DataFrame(data)\n",
    "\n",
    "    print(df.head())\n",
    "\n",
    "\n",
    "    return df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "def download_images_from_df(df, url_column='photo_url', latitude_column='latitude', longitude_column='longitude', save_folder='Images', save_csv=False, csv_file_name='output.csv'):\n",
    "    \"\"\"\n",
    "    Download images from a DataFrame and save them locally in a specified folder.\n",
    "\n",
    "    Parameters:\n",
    "    - df: DataFrame containing image URLs, latitudes, and longitudes.\n",
    "    - url_column: str, name of the column containing the image URLs (default is 'photo_url').\n",
    "    - latitude_column: str, name of the column containing the latitudes (default is 'latitude').\n",
    "    - longitude_column: str, name of the column containing the longitudes (default is 'longitude').\n",
    "    - save_folder: str, folder where the images will be saved (default is 'Images').\n",
    "\n",
    "    Returns:\n",
    "    - df: The updated DataFrame with the 'image_path' column.\n",
    "    \"\"\"\n",
    "    # Create a folder to save images if it doesn't already exist\n",
    "    os.makedirs(save_folder, exist_ok=True)\n",
    "    print(f\"Images will be saved in: {save_folder}\")\n",
    "\n",
    "    # Dictionary to count occurrences of each latitude/longitude combination\n",
    "    counter = {}\n",
    "\n",
    "    # Iterate through the DataFrame row by row\n",
    "    for index, row in df.iterrows():\n",
    "        # Extract the image URL, latitude, and longitude from the current row\n",
    "        image_url = row[url_column]\n",
    "        latitude = row[latitude_column]\n",
    "        longitude = row[longitude_column]\n",
    "\n",
    "        # Create a unique key for the latitude and longitude\n",
    "        location_key = f\"{latitude}_{longitude}\"\n",
    "\n",
    "        # Increment the counter for each unique location\n",
    "        if location_key in counter:\n",
    "            counter[location_key] += 1\n",
    "        else:\n",
    "            counter[location_key] = 1\n",
    "\n",
    "        # Define the image file name using latitude, longitude, and the counter\n",
    "        image_name = os.path.join(save_folder, f\"{latitude}_{longitude}_{counter[location_key]}.jpg\")\n",
    "\n",
    "        try:\n",
    "            # Send a GET request to the image URL with a timeout of 10 seconds\n",
    "            response = requests.get(image_url, timeout=10)\n",
    "\n",
    "            # Check if the response indicates success (status code 200)\n",
    "            if response.status_code == 200:\n",
    "                # Save the image content to the specified file\n",
    "                with open(image_name, 'wb') as file:\n",
    "                    file.write(response.content)\n",
    "                print(f\"Downloaded: {image_name}\")\n",
    "\n",
    "                # Update the 'image_path' column in the DataFrame with the saved image path\n",
    "                df.at[index, 'image_path'] = image_name\n",
    "            elif response.status_code == 400:\n",
    "                # Handle bad request errors\n",
    "                print(f\"Skipping image from {image_url} (status code: {response.status_code})\")\n",
    "            else:\n",
    "                # Handle other unsuccessful status codes\n",
    "                print(f\"Failed to download image from {image_url} (status code: {response.status_code})\")\n",
    "        except Exception as e:\n",
    "            # Handle any exceptions that occur during the request\n",
    "            print(f\"Error downloading image from {image_url}: {e}\")\n",
    "\n",
    "    # If saving the updated DataFrame as a CSV file is desired, do that\n",
    "    if save_csv:\n",
    "        df.to_csv(csv_file_name, index=False)\n",
    "        print(f\"DataFrame saved to {csv_file_name}\")\n",
    "\n",
    "    return df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "def save_semi_clean_data(df, lat_column='latitude', lon_column='longitude', image_path_column='image_path', output_file='semi_clean_data.csv'):\n",
    "    \"\"\"\n",
    "    Save a DataFrame with only latitude, longitude, and image path to a CSV file in the current directory.\n",
    "\n",
    "    Parameters:\n",
    "    - df: DataFrame containing the original data.\n",
    "    - lat_column: str, name of the column containing latitudes (default is 'latitude').\n",
    "    - lon_column: str, name of the column containing longitudes (default is 'longitude').\n",
    "    - image_path_column: str, name of the column containing image paths (default is 'image_path').\n",
    "    - output_file: str, name of the output CSV file (default is 'semi_clean_data.csv').\n",
    "    \"\"\"\n",
    "    # select only the columns interested in\n",
    "    semi_clean_df = df[[lat_column, lon_column, image_path_column]]\n",
    "\n",
    "    # Get the current working directory  to save the file\n",
    "    current_directory = os.getcwd()\n",
    "\n",
    "    # Create the full path for the output file with the specified name\n",
    "    output_path = os.path.join(current_directory, output_file)\n",
    "\n",
    "    # Save the new DataFrame to a CSV file at the specified location\n",
    "    semi_clean_df.to_csv(output_path, index=False)\n",
    "    print(f\"Semi-clean data saved to {output_path}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "ename": "FileNotFoundError",
     "evalue": "[Errno 2] No such file or directory: ''",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[6], line 5\u001b[0m\n\u001b[1;32m      3\u001b[0m file_path \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m      4\u001b[0m \u001b[38;5;66;03m#  path up^^^^^^\u001b[39;00m\n\u001b[0;32m----> 5\u001b[0m df \u001b[38;5;241m=\u001b[39m \u001b[43mjson_to_dataframe\u001b[49m\u001b[43m(\u001b[49m\u001b[43mfile_path\u001b[49m\u001b[43m)\u001b[49m\n",
      "Cell \u001b[0;32mIn[3], line 12\u001b[0m, in \u001b[0;36mjson_to_dataframe\u001b[0;34m(file_path)\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mjson_to_dataframe\u001b[39m(file_path):\n\u001b[1;32m      2\u001b[0m \u001b[38;5;250m    \u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[1;32m      3\u001b[0m \u001b[38;5;124;03m    Read a JSON file and convert it to a Pandas DataFrame.\u001b[39;00m\n\u001b[1;32m      4\u001b[0m \n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m     10\u001b[0m \u001b[38;5;124;03m    - DataFrame containing the JSON data.\u001b[39;00m\n\u001b[1;32m     11\u001b[0m \u001b[38;5;124;03m    \"\"\"\u001b[39;00m\n\u001b[0;32m---> 12\u001b[0m     \u001b[38;5;28;01mwith\u001b[39;00m \u001b[38;5;28;43mopen\u001b[39;49m\u001b[43m(\u001b[49m\u001b[43mfile_path\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mr\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mencoding\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mutf-8\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m)\u001b[49m \u001b[38;5;28;01mas\u001b[39;00m file:\n\u001b[1;32m     13\u001b[0m         data \u001b[38;5;241m=\u001b[39m json\u001b[38;5;241m.\u001b[39mload(file)\n\u001b[1;32m     15\u001b[0m     df \u001b[38;5;241m=\u001b[39m pd\u001b[38;5;241m.\u001b[39mDataFrame(data)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/IPython/core/interactiveshell.py:324\u001b[0m, in \u001b[0;36m_modified_open\u001b[0;34m(file, *args, **kwargs)\u001b[0m\n\u001b[1;32m    317\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m file \u001b[38;5;129;01min\u001b[39;00m {\u001b[38;5;241m0\u001b[39m, \u001b[38;5;241m1\u001b[39m, \u001b[38;5;241m2\u001b[39m}:\n\u001b[1;32m    318\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[1;32m    319\u001b[0m         \u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mIPython won\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mt let you open fd=\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mfile\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m by default \u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m    320\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mas it is likely to crash IPython. If you know what you are doing, \u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m    321\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124myou can use builtins\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124m open.\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m    322\u001b[0m     )\n\u001b[0;32m--> 324\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mio_open\u001b[49m\u001b[43m(\u001b[49m\u001b[43mfile\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: ''"
     ]
    }
   ],
   "source": [
    "# Example usage of json_to_dataframe()\n",
    "#file_path = \"Outscraper-20241011183106xs96_fine_dining_restaurant.json\"\n",
    "file_path = \"\"\n",
    "#  path up^^^^^^\n",
    "df = json_to_dataframe(file_path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Example DataFrame setup (replace this with the actual DataFrame)\n",
    "# Call the function to download images from the DataFrame\n",
    "df_p = download_images_from_df(df, save_csv=True, csv_file_name='geo_pic.csv')\n",
    "# Display the updated DataFrame\n",
    "print(df_p)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Example usage of save_semi_clean_data():\n",
    "# I have 'geo_pic.csv' as my input file, which will be loaded into a DataFrame\n",
    "#file_path = \"geo_pic.csv\"\n",
    "file_path = \"\"\n",
    "# Load the DataFrame from the CSV file\n",
    "df = pd.read_csv(file_path)\n",
    "# Call the function to save the semi-clean data  just created\n",
    "save_semi_clean_data(df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/mohammed/.pyenv/versions/geo-pic/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html\n",
      "  from .autonotebook import tqdm as notebook_tqdm\n"
     ]
    },
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[1], line 4\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mtorch\u001b[39;00m\n\u001b[1;32m      2\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mgeoclip\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m GeoCLIP\n\u001b[0;32m----> 4\u001b[0m model \u001b[38;5;241m=\u001b[39m \u001b[43mGeoCLIP\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m      6\u001b[0m image_path \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mimage.png\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m      8\u001b[0m top_pred_gps, top_pred_prob \u001b[38;5;241m=\u001b[39m model\u001b[38;5;241m.\u001b[39mpredict(image_path, top_k\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m5\u001b[39m)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/geoclip/model/GeoCLIP.py:17\u001b[0m, in \u001b[0;36mGeoCLIP.__init__\u001b[0;34m(self, from_pretrained, queue_size)\u001b[0m\n\u001b[1;32m     15\u001b[0m \u001b[38;5;28msuper\u001b[39m()\u001b[38;5;241m.\u001b[39m\u001b[38;5;21m__init__\u001b[39m()\n\u001b[1;32m     16\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlogit_scale \u001b[38;5;241m=\u001b[39m nn\u001b[38;5;241m.\u001b[39mParameter(torch\u001b[38;5;241m.\u001b[39mones([]) \u001b[38;5;241m*\u001b[39m np\u001b[38;5;241m.\u001b[39mlog(\u001b[38;5;241m1\u001b[39m \u001b[38;5;241m/\u001b[39m \u001b[38;5;241m0.07\u001b[39m))\n\u001b[0;32m---> 17\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mimage_encoder \u001b[38;5;241m=\u001b[39m \u001b[43mImageEncoder\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m     18\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlocation_encoder \u001b[38;5;241m=\u001b[39m LocationEncoder()\n\u001b[1;32m     20\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mgps_gallery \u001b[38;5;241m=\u001b[39m load_gps_data(os\u001b[38;5;241m.\u001b[39mpath\u001b[38;5;241m.\u001b[39mjoin(file_dir, \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mgps_gallery\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mcoordinates_100K.csv\u001b[39m\u001b[38;5;124m\"\u001b[39m))\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/geoclip/model/image_encoder.py:11\u001b[0m, in \u001b[0;36mImageEncoder.__init__\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m      9\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21m__init__\u001b[39m(\u001b[38;5;28mself\u001b[39m):\n\u001b[1;32m     10\u001b[0m     \u001b[38;5;28msuper\u001b[39m(ImageEncoder, \u001b[38;5;28mself\u001b[39m)\u001b[38;5;241m.\u001b[39m\u001b[38;5;21m__init__\u001b[39m()\n\u001b[0;32m---> 11\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mCLIP \u001b[38;5;241m=\u001b[39m \u001b[43mCLIPModel\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mfrom_pretrained\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mopenai/clip-vit-large-patch14\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m)\u001b[49m\n\u001b[1;32m     12\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mimage_processor \u001b[38;5;241m=\u001b[39m AutoProcessor\u001b[38;5;241m.\u001b[39mfrom_pretrained(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mopenai/clip-vit-large-patch14\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m     13\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mmlp \u001b[38;5;241m=\u001b[39m nn\u001b[38;5;241m.\u001b[39mSequential(nn\u001b[38;5;241m.\u001b[39mLinear(\u001b[38;5;241m768\u001b[39m, \u001b[38;5;241m768\u001b[39m),\n\u001b[1;32m     14\u001b[0m                              nn\u001b[38;5;241m.\u001b[39mReLU(),\n\u001b[1;32m     15\u001b[0m                              nn\u001b[38;5;241m.\u001b[39mLinear(\u001b[38;5;241m768\u001b[39m, \u001b[38;5;241m512\u001b[39m))\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/transformers/modeling_utils.py:3604\u001b[0m, in \u001b[0;36mPreTrainedModel.from_pretrained\u001b[0;34m(cls, pretrained_model_name_or_path, config, cache_dir, ignore_mismatched_sizes, force_download, local_files_only, token, revision, use_safetensors, *model_args, **kwargs)\u001b[0m\n\u001b[1;32m   3588\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[1;32m   3589\u001b[0m     \u001b[38;5;66;03m# Load from URL or cache if already cached\u001b[39;00m\n\u001b[1;32m   3590\u001b[0m     cached_file_kwargs \u001b[38;5;241m=\u001b[39m {\n\u001b[1;32m   3591\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mcache_dir\u001b[39m\u001b[38;5;124m\"\u001b[39m: cache_dir,\n\u001b[1;32m   3592\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mforce_download\u001b[39m\u001b[38;5;124m\"\u001b[39m: force_download,\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m   3602\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m_commit_hash\u001b[39m\u001b[38;5;124m\"\u001b[39m: commit_hash,\n\u001b[1;32m   3603\u001b[0m     }\n\u001b[0;32m-> 3604\u001b[0m     resolved_archive_file \u001b[38;5;241m=\u001b[39m \u001b[43mcached_file\u001b[49m\u001b[43m(\u001b[49m\u001b[43mpretrained_model_name_or_path\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mfilename\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mcached_file_kwargs\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   3606\u001b[0m     \u001b[38;5;66;03m# Since we set _raise_exceptions_for_missing_entries=False, we don't get an exception but a None\u001b[39;00m\n\u001b[1;32m   3607\u001b[0m     \u001b[38;5;66;03m# result when internet is up, the repo and revision exist, but the file does not.\u001b[39;00m\n\u001b[1;32m   3608\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m resolved_archive_file \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;129;01mand\u001b[39;00m filename \u001b[38;5;241m==\u001b[39m _add_variant(SAFE_WEIGHTS_NAME, variant):\n\u001b[1;32m   3609\u001b[0m         \u001b[38;5;66;03m# Maybe the checkpoint is sharded, we try to grab the index name in this case.\u001b[39;00m\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/transformers/utils/hub.py:403\u001b[0m, in \u001b[0;36mcached_file\u001b[0;34m(path_or_repo_id, filename, cache_dir, force_download, resume_download, proxies, token, revision, local_files_only, subfolder, repo_type, user_agent, _raise_exceptions_for_gated_repo, _raise_exceptions_for_missing_entries, _raise_exceptions_for_connection_errors, _commit_hash, **deprecated_kwargs)\u001b[0m\n\u001b[1;32m    400\u001b[0m user_agent \u001b[38;5;241m=\u001b[39m http_user_agent(user_agent)\n\u001b[1;32m    401\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[1;32m    402\u001b[0m     \u001b[38;5;66;03m# Load from URL or cache if already cached\u001b[39;00m\n\u001b[0;32m--> 403\u001b[0m     resolved_file \u001b[38;5;241m=\u001b[39m \u001b[43mhf_hub_download\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m    404\u001b[0m \u001b[43m        \u001b[49m\u001b[43mpath_or_repo_id\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    405\u001b[0m \u001b[43m        \u001b[49m\u001b[43mfilename\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    406\u001b[0m \u001b[43m        \u001b[49m\u001b[43msubfolder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;28;43;01mNone\u001b[39;49;00m\u001b[43m \u001b[49m\u001b[38;5;28;43;01mif\u001b[39;49;00m\u001b[43m \u001b[49m\u001b[38;5;28;43mlen\u001b[39;49m\u001b[43m(\u001b[49m\u001b[43msubfolder\u001b[49m\u001b[43m)\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m==\u001b[39;49m\u001b[43m \u001b[49m\u001b[38;5;241;43m0\u001b[39;49m\u001b[43m \u001b[49m\u001b[38;5;28;43;01melse\u001b[39;49;00m\u001b[43m \u001b[49m\u001b[43msubfolder\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    407\u001b[0m \u001b[43m        \u001b[49m\u001b[43mrepo_type\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mrepo_type\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    408\u001b[0m \u001b[43m        \u001b[49m\u001b[43mrevision\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mrevision\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    409\u001b[0m \u001b[43m        \u001b[49m\u001b[43mcache_dir\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mcache_dir\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    410\u001b[0m \u001b[43m        \u001b[49m\u001b[43muser_agent\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43muser_agent\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    411\u001b[0m \u001b[43m        \u001b[49m\u001b[43mforce_download\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mforce_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    412\u001b[0m \u001b[43m        \u001b[49m\u001b[43mproxies\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mproxies\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    413\u001b[0m \u001b[43m        \u001b[49m\u001b[43mresume_download\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mresume_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    414\u001b[0m \u001b[43m        \u001b[49m\u001b[43mtoken\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mtoken\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    415\u001b[0m \u001b[43m        \u001b[49m\u001b[43mlocal_files_only\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mlocal_files_only\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m    416\u001b[0m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    417\u001b[0m \u001b[38;5;28;01mexcept\u001b[39;00m GatedRepoError \u001b[38;5;28;01mas\u001b[39;00m e:\n\u001b[1;32m    418\u001b[0m     resolved_file \u001b[38;5;241m=\u001b[39m _get_cache_file_to_return(path_or_repo_id, full_filename, cache_dir, revision)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/utils/_deprecation.py:101\u001b[0m, in \u001b[0;36m_deprecate_arguments.<locals>._inner_deprecate_positional_args.<locals>.inner_f\u001b[0;34m(*args, **kwargs)\u001b[0m\n\u001b[1;32m     99\u001b[0m         message \u001b[38;5;241m+\u001b[39m\u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;241m+\u001b[39m custom_message\n\u001b[1;32m    100\u001b[0m     warnings\u001b[38;5;241m.\u001b[39mwarn(message, \u001b[38;5;167;01mFutureWarning\u001b[39;00m)\n\u001b[0;32m--> 101\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mf\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py:114\u001b[0m, in \u001b[0;36mvalidate_hf_hub_args.<locals>._inner_fn\u001b[0;34m(*args, **kwargs)\u001b[0m\n\u001b[1;32m    111\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m check_use_auth_token:\n\u001b[1;32m    112\u001b[0m     kwargs \u001b[38;5;241m=\u001b[39m smoothly_deprecate_use_auth_token(fn_name\u001b[38;5;241m=\u001b[39mfn\u001b[38;5;241m.\u001b[39m\u001b[38;5;18m__name__\u001b[39m, has_token\u001b[38;5;241m=\u001b[39mhas_token, kwargs\u001b[38;5;241m=\u001b[39mkwargs)\n\u001b[0;32m--> 114\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mfn\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/file_download.py:1232\u001b[0m, in \u001b[0;36mhf_hub_download\u001b[0;34m(repo_id, filename, subfolder, repo_type, revision, library_name, library_version, cache_dir, local_dir, user_agent, force_download, proxies, etag_timeout, token, local_files_only, headers, endpoint, legacy_cache_layout, resume_download, force_filename, local_dir_use_symlinks)\u001b[0m\n\u001b[1;32m   1212\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m _hf_hub_download_to_local_dir(\n\u001b[1;32m   1213\u001b[0m         \u001b[38;5;66;03m# Destination\u001b[39;00m\n\u001b[1;32m   1214\u001b[0m         local_dir\u001b[38;5;241m=\u001b[39mlocal_dir,\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m   1229\u001b[0m         local_files_only\u001b[38;5;241m=\u001b[39mlocal_files_only,\n\u001b[1;32m   1230\u001b[0m     )\n\u001b[1;32m   1231\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m-> 1232\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43m_hf_hub_download_to_cache_dir\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m   1233\u001b[0m \u001b[43m        \u001b[49m\u001b[38;5;66;43;03m# Destination\u001b[39;49;00m\n\u001b[1;32m   1234\u001b[0m \u001b[43m        \u001b[49m\u001b[43mcache_dir\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mcache_dir\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1235\u001b[0m \u001b[43m        \u001b[49m\u001b[38;5;66;43;03m# File info\u001b[39;49;00m\n\u001b[1;32m   1236\u001b[0m \u001b[43m        \u001b[49m\u001b[43mrepo_id\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mrepo_id\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1237\u001b[0m \u001b[43m        \u001b[49m\u001b[43mfilename\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mfilename\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1238\u001b[0m \u001b[43m        \u001b[49m\u001b[43mrepo_type\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mrepo_type\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1239\u001b[0m \u001b[43m        \u001b[49m\u001b[43mrevision\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mrevision\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1240\u001b[0m \u001b[43m        \u001b[49m\u001b[38;5;66;43;03m# HTTP info\u001b[39;49;00m\n\u001b[1;32m   1241\u001b[0m \u001b[43m        \u001b[49m\u001b[43mendpoint\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mendpoint\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1242\u001b[0m \u001b[43m        \u001b[49m\u001b[43metag_timeout\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43metag_timeout\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1243\u001b[0m \u001b[43m        \u001b[49m\u001b[43mheaders\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mheaders\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1244\u001b[0m \u001b[43m        \u001b[49m\u001b[43mproxies\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mproxies\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1245\u001b[0m \u001b[43m        \u001b[49m\u001b[43mtoken\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mtoken\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1246\u001b[0m \u001b[43m        \u001b[49m\u001b[38;5;66;43;03m# Additional options\u001b[39;49;00m\n\u001b[1;32m   1247\u001b[0m \u001b[43m        \u001b[49m\u001b[43mlocal_files_only\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mlocal_files_only\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1248\u001b[0m \u001b[43m        \u001b[49m\u001b[43mforce_download\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mforce_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1249\u001b[0m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/file_download.py:1381\u001b[0m, in \u001b[0;36m_hf_hub_download_to_cache_dir\u001b[0;34m(cache_dir, repo_id, filename, repo_type, revision, endpoint, etag_timeout, headers, proxies, token, local_files_only, force_download)\u001b[0m\n\u001b[1;32m   1379\u001b[0m Path(lock_path)\u001b[38;5;241m.\u001b[39mparent\u001b[38;5;241m.\u001b[39mmkdir(parents\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m, exist_ok\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m)\n\u001b[1;32m   1380\u001b[0m \u001b[38;5;28;01mwith\u001b[39;00m WeakFileLock(lock_path):\n\u001b[0;32m-> 1381\u001b[0m     \u001b[43m_download_to_tmp_and_move\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m   1382\u001b[0m \u001b[43m        \u001b[49m\u001b[43mincomplete_path\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mPath\u001b[49m\u001b[43m(\u001b[49m\u001b[43mblob_path\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m+\u001b[39;49m\u001b[43m \u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43m.incomplete\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1383\u001b[0m \u001b[43m        \u001b[49m\u001b[43mdestination_path\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mPath\u001b[49m\u001b[43m(\u001b[49m\u001b[43mblob_path\u001b[49m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1384\u001b[0m \u001b[43m        \u001b[49m\u001b[43murl_to_download\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43murl_to_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1385\u001b[0m \u001b[43m        \u001b[49m\u001b[43mproxies\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mproxies\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1386\u001b[0m \u001b[43m        \u001b[49m\u001b[43mheaders\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mheaders\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1387\u001b[0m \u001b[43m        \u001b[49m\u001b[43mexpected_size\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mexpected_size\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1388\u001b[0m \u001b[43m        \u001b[49m\u001b[43mfilename\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mfilename\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1389\u001b[0m \u001b[43m        \u001b[49m\u001b[43mforce_download\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mforce_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1390\u001b[0m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1391\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m os\u001b[38;5;241m.\u001b[39mpath\u001b[38;5;241m.\u001b[39mexists(pointer_path):\n\u001b[1;32m   1392\u001b[0m         _create_symlink(blob_path, pointer_path, new_blob\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/file_download.py:1915\u001b[0m, in \u001b[0;36m_download_to_tmp_and_move\u001b[0;34m(incomplete_path, destination_path, url_to_download, proxies, headers, expected_size, filename, force_download)\u001b[0m\n\u001b[1;32m   1912\u001b[0m         _check_disk_space(expected_size, incomplete_path\u001b[38;5;241m.\u001b[39mparent)\n\u001b[1;32m   1913\u001b[0m         _check_disk_space(expected_size, destination_path\u001b[38;5;241m.\u001b[39mparent)\n\u001b[0;32m-> 1915\u001b[0m     \u001b[43mhttp_get\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m   1916\u001b[0m \u001b[43m        \u001b[49m\u001b[43murl_to_download\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1917\u001b[0m \u001b[43m        \u001b[49m\u001b[43mf\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1918\u001b[0m \u001b[43m        \u001b[49m\u001b[43mproxies\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mproxies\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1919\u001b[0m \u001b[43m        \u001b[49m\u001b[43mresume_size\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mresume_size\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1920\u001b[0m \u001b[43m        \u001b[49m\u001b[43mheaders\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mheaders\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1921\u001b[0m \u001b[43m        \u001b[49m\u001b[43mexpected_size\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mexpected_size\u001b[49m\u001b[43m,\u001b[49m\n\u001b[1;32m   1922\u001b[0m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1924\u001b[0m logger\u001b[38;5;241m.\u001b[39minfo(\u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mDownload complete. Moving file to \u001b[39m\u001b[38;5;132;01m{\u001b[39;00mdestination_path\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m   1925\u001b[0m _chmod_and_move(incomplete_path, destination_path)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/huggingface_hub/file_download.py:541\u001b[0m, in \u001b[0;36mhttp_get\u001b[0;34m(url, temp_file, proxies, resume_size, headers, expected_size, displayed_filename, _nb_retries, _tqdm_bar)\u001b[0m\n\u001b[1;32m    539\u001b[0m new_resume_size \u001b[38;5;241m=\u001b[39m resume_size\n\u001b[1;32m    540\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[0;32m--> 541\u001b[0m     \u001b[38;5;28;01mfor\u001b[39;00m chunk \u001b[38;5;129;01min\u001b[39;00m r\u001b[38;5;241m.\u001b[39miter_content(chunk_size\u001b[38;5;241m=\u001b[39mconstants\u001b[38;5;241m.\u001b[39mDOWNLOAD_CHUNK_SIZE):\n\u001b[1;32m    542\u001b[0m         \u001b[38;5;28;01mif\u001b[39;00m chunk:  \u001b[38;5;66;03m# filter out keep-alive new chunks\u001b[39;00m\n\u001b[1;32m    543\u001b[0m             progress\u001b[38;5;241m.\u001b[39mupdate(\u001b[38;5;28mlen\u001b[39m(chunk))\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/requests/models.py:820\u001b[0m, in \u001b[0;36mResponse.iter_content.<locals>.generate\u001b[0;34m()\u001b[0m\n\u001b[1;32m    818\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mhasattr\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mraw, \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mstream\u001b[39m\u001b[38;5;124m\"\u001b[39m):\n\u001b[1;32m    819\u001b[0m     \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[0;32m--> 820\u001b[0m         \u001b[38;5;28;01myield from\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mraw\u001b[38;5;241m.\u001b[39mstream(chunk_size, decode_content\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m)\n\u001b[1;32m    821\u001b[0m     \u001b[38;5;28;01mexcept\u001b[39;00m ProtocolError \u001b[38;5;28;01mas\u001b[39;00m e:\n\u001b[1;32m    822\u001b[0m         \u001b[38;5;28;01mraise\u001b[39;00m ChunkedEncodingError(e)\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/urllib3/response.py:1060\u001b[0m, in \u001b[0;36mHTTPResponse.stream\u001b[0;34m(self, amt, decode_content)\u001b[0m\n\u001b[1;32m   1058\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m   1059\u001b[0m     \u001b[38;5;28;01mwhile\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m is_fp_closed(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp) \u001b[38;5;129;01mor\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_decoded_buffer) \u001b[38;5;241m>\u001b[39m \u001b[38;5;241m0\u001b[39m:\n\u001b[0;32m-> 1060\u001b[0m         data \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[43mamt\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mamt\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdecode_content\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdecode_content\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1062\u001b[0m         \u001b[38;5;28;01mif\u001b[39;00m data:\n\u001b[1;32m   1063\u001b[0m             \u001b[38;5;28;01myield\u001b[39;00m data\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/urllib3/response.py:949\u001b[0m, in \u001b[0;36mHTTPResponse.read\u001b[0;34m(self, amt, decode_content, cache_content)\u001b[0m\n\u001b[1;32m    946\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_decoded_buffer) \u001b[38;5;241m>\u001b[39m\u001b[38;5;241m=\u001b[39m amt:\n\u001b[1;32m    947\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_decoded_buffer\u001b[38;5;241m.\u001b[39mget(amt)\n\u001b[0;32m--> 949\u001b[0m data \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_raw_read\u001b[49m\u001b[43m(\u001b[49m\u001b[43mamt\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    951\u001b[0m flush_decoder \u001b[38;5;241m=\u001b[39m amt \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;129;01mor\u001b[39;00m (amt \u001b[38;5;241m!=\u001b[39m \u001b[38;5;241m0\u001b[39m \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m data)\n\u001b[1;32m    953\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m data \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_decoded_buffer) \u001b[38;5;241m==\u001b[39m \u001b[38;5;241m0\u001b[39m:\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/urllib3/response.py:873\u001b[0m, in \u001b[0;36mHTTPResponse._raw_read\u001b[0;34m(self, amt, read1)\u001b[0m\n\u001b[1;32m    870\u001b[0m fp_closed \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mgetattr\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp, \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mclosed\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mFalse\u001b[39;00m)\n\u001b[1;32m    872\u001b[0m \u001b[38;5;28;01mwith\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_error_catcher():\n\u001b[0;32m--> 873\u001b[0m     data \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_fp_read\u001b[49m\u001b[43m(\u001b[49m\u001b[43mamt\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mread1\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mread1\u001b[49m\u001b[43m)\u001b[49m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m fp_closed \u001b[38;5;28;01melse\u001b[39;00m \u001b[38;5;124mb\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m    874\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m amt \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;129;01mand\u001b[39;00m amt \u001b[38;5;241m!=\u001b[39m \u001b[38;5;241m0\u001b[39m \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m data:\n\u001b[1;32m    875\u001b[0m         \u001b[38;5;66;03m# Platform-specific: Buggy versions of Python.\u001b[39;00m\n\u001b[1;32m    876\u001b[0m         \u001b[38;5;66;03m# Close the connection when no data is returned\u001b[39;00m\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m    881\u001b[0m         \u001b[38;5;66;03m# not properly close the connection in all cases. There is\u001b[39;00m\n\u001b[1;32m    882\u001b[0m         \u001b[38;5;66;03m# no harm in redundantly calling close.\u001b[39;00m\n\u001b[1;32m    883\u001b[0m         \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp\u001b[38;5;241m.\u001b[39mclose()\n",
      "File \u001b[0;32m~/.pyenv/versions/geo-pic/lib/python3.10/site-packages/urllib3/response.py:856\u001b[0m, in \u001b[0;36mHTTPResponse._fp_read\u001b[0;34m(self, amt, read1)\u001b[0m\n\u001b[1;32m    853\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp\u001b[38;5;241m.\u001b[39mread1(amt) \u001b[38;5;28;01mif\u001b[39;00m amt \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;28;01melse\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp\u001b[38;5;241m.\u001b[39mread1()\n\u001b[1;32m    854\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m    855\u001b[0m     \u001b[38;5;66;03m# StringIO doesn't like amt=None\u001b[39;00m\n\u001b[0;32m--> 856\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_fp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[43mamt\u001b[49m\u001b[43m)\u001b[49m \u001b[38;5;28;01mif\u001b[39;00m amt \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;28;01melse\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_fp\u001b[38;5;241m.\u001b[39mread()\n",
      "File \u001b[0;32m~/.pyenv/versions/3.10.6/lib/python3.10/http/client.py:465\u001b[0m, in \u001b[0;36mHTTPResponse.read\u001b[0;34m(self, amt)\u001b[0m\n\u001b[1;32m    462\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlength \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;129;01mand\u001b[39;00m amt \u001b[38;5;241m>\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlength:\n\u001b[1;32m    463\u001b[0m     \u001b[38;5;66;03m# clip the read to the \"end of response\"\u001b[39;00m\n\u001b[1;32m    464\u001b[0m     amt \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlength\n\u001b[0;32m--> 465\u001b[0m s \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mfp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[43mamt\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    466\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m s \u001b[38;5;129;01mand\u001b[39;00m amt:\n\u001b[1;32m    467\u001b[0m     \u001b[38;5;66;03m# Ideally, we would raise IncompleteRead if the content-length\u001b[39;00m\n\u001b[1;32m    468\u001b[0m     \u001b[38;5;66;03m# wasn't satisfied, but it might break compatibility.\u001b[39;00m\n\u001b[1;32m    469\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_close_conn()\n",
      "File \u001b[0;32m~/.pyenv/versions/3.10.6/lib/python3.10/socket.py:705\u001b[0m, in \u001b[0;36mSocketIO.readinto\u001b[0;34m(self, b)\u001b[0m\n\u001b[1;32m    703\u001b[0m \u001b[38;5;28;01mwhile\u001b[39;00m \u001b[38;5;28;01mTrue\u001b[39;00m:\n\u001b[1;32m    704\u001b[0m     \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[0;32m--> 705\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_sock\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mrecv_into\u001b[49m\u001b[43m(\u001b[49m\u001b[43mb\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    706\u001b[0m     \u001b[38;5;28;01mexcept\u001b[39;00m timeout:\n\u001b[1;32m    707\u001b[0m         \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_timeout_occurred \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;01mTrue\u001b[39;00m\n",
      "File \u001b[0;32m~/.pyenv/versions/3.10.6/lib/python3.10/ssl.py:1274\u001b[0m, in \u001b[0;36mSSLSocket.recv_into\u001b[0;34m(self, buffer, nbytes, flags)\u001b[0m\n\u001b[1;32m   1270\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m flags \u001b[38;5;241m!=\u001b[39m \u001b[38;5;241m0\u001b[39m:\n\u001b[1;32m   1271\u001b[0m         \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[1;32m   1272\u001b[0m           \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mnon-zero flags not allowed in calls to recv_into() on \u001b[39m\u001b[38;5;132;01m%s\u001b[39;00m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;241m%\u001b[39m\n\u001b[1;32m   1273\u001b[0m           \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m\u001b[38;5;18m__class__\u001b[39m)\n\u001b[0;32m-> 1274\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[43mnbytes\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mbuffer\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1275\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m   1276\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28msuper\u001b[39m()\u001b[38;5;241m.\u001b[39mrecv_into(buffer, nbytes, flags)\n",
      "File \u001b[0;32m~/.pyenv/versions/3.10.6/lib/python3.10/ssl.py:1130\u001b[0m, in \u001b[0;36mSSLSocket.read\u001b[0;34m(self, len, buffer)\u001b[0m\n\u001b[1;32m   1128\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[1;32m   1129\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m buffer \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[0;32m-> 1130\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_sslobj\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;28;43mlen\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mbuffer\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1131\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m   1132\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_sslobj\u001b[38;5;241m.\u001b[39mread(\u001b[38;5;28mlen\u001b[39m)\n",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "import torch\n",
    "from geoclip import GeoCLIP\n",
    "\n",
    "model = GeoCLIP()\n",
    "\n",
    "image_path = \"image.png\"\n",
    "\n",
    "top_pred_gps, top_pred_prob = model.predict(image_path, top_k=5)\n",
    "\n",
    "print(\"Top 5 GPS Predictions\")\n",
    "print(\"=====================\")\n",
    "for i in range(5):\n",
    "    lat, lon = top_pred_gps[i]\n",
    "    print(f\"Prediction {i+1}: ({lat:.6f}, {lon:.6f})\")\n",
    "    print(f\"Probability: {top_pred_prob[i]:.6f}\")\n",
    "    print(\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "geo-pic",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
