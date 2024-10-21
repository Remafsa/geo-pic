from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import pandas as pd
from dotenv import load_dotenv
from recommendation_system.ml_logic import find_similar_images
from scripts import get_place_id, get_place_details,get_nearby_places,extract_reviews,get_place_details, get_photo_references,convert_timestamp_to_date,save_results_to_json
from tensorflow.keras.applications import ResNet50
from Content_based_Recommender import (process_sentences, recommend,get_name_recommendation,get_city_recommendation,get_similarity_recommendation)

load_dotenv()

api_key = os.getenv('API_KEY')

app = FastAPI()

# Define paths for the CSV files
current_dir = os.path.dirname(os.path.abspath(__file__))
image_features_path = os.path.join(current_dir, "..", "notebooks", "image_features.csv")
output_images_path = os.path.join(current_dir, "..", "notebooks", "output_images.csv")

# Load the image features CSV
df_features = pd.read_csv(image_features_path)
# Load the output images CSV
df_output = pd.read_csv(output_images_path)

# Debugging: Check columns
print("Image Features DataFrame columns:", df_features.columns)
print("Output Images DataFrame columns:", df_output.columns)

# Ensure IMG_FILE is in both DataFrames
if 'IMG_FILE' not in df_features.columns or 'IMG_FILE' not in df_output.columns:
    raise KeyError("'IMG_FILE' column not found in one of the DataFrames.")

# Load image features
image_features = df_features.iloc[:, 1:].values  # Assuming features start from the second column
local_image_paths = df_features['IMG_FILE'].tolist()

@app.get("/recommendation/")
def get_recommendation(user_input: str):
    # Get recommendations based on user input
    recommend_result = recommend(user_input)
    name = get_name_recommendation(recommend_result)
    area = get_city_recommendation(recommend_result)

    place_id = get_place_id(api_key, restaurant_name=name, area=area)
    place_details = get_place_details(api_key, place_id=place_id)

    return {
        "name": name,
        "area": area,
        "place_id": place_id,
        "details": place_details
    }

@app.post("/find_similar/")
async def find_similar(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    # Find similar images
    similar_images = find_similar_images(temp_file_path, image_features, df_features, model, n_similar=10)

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Prepare the results
    results = []
    for sim_score, sim_img in similar_images:
        # Find the row in the output images DataFrame
        row = df_output[df_output['IMG_FILE'] == sim_img]

        # Check if the row exists
        if not row.empty:
            row = row.iloc[0]
            result = {
                "image_path": sim_img,
                "name": row['name'],  # Access name from output_images.csv
                "image_url": row['photo_url'],
                "cosine_similarity": sim_score
            }
            results.append(result)
        else:
            print(f"Warning: Image '{sim_img}' not found in the output images DataFrame.")

    return JSONResponse(content={"similar_images": results})

@app.get("/")
def root():
    return {'greeting': 'Hello'}
