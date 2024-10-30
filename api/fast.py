from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import pandas as pd
from dotenv import load_dotenv
from recommendation_system.ml_logic import find_similar_images
from scripts import *
from tensorflow.keras.applications import ResNet50
from Content_based_Recommender import process_sentences, recommend,get_name_recommendation,get_city_recommendation,get_similarity_recommendation
from summary_sentiment import *

load_dotenv()

api_key = os.getenv('API_KEY')

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
image_features_path = os.path.join(current_dir, "..", "notebooks", "image_features.csv")
output_images_path = os.path.join(current_dir, "..", "notebooks", "output_images.csv")

df_features = pd.read_csv(image_features_path)
df_output = pd.read_csv(output_images_path)
print(df_output.columns)

if 'IMG_FILE' not in df_features.columns or 'IMG_FILE' not in df_output.columns:
    raise KeyError("'IMG_FILE' column not found in one of the DataFrames.")

image_features = df_features.iloc[:, 1:].values


@app.get("/recommendation/")
def get_recommendation(user_input: str):

    # Get recommendations based on user input
    recommend_result = recommend(user_input)

    # Get top 3 results
    names = get_name_recommendation(recommend_result)
    areas = get_city_recommendation(recommend_result)
    similarities = get_similarity_recommendation(recommend_result)

    results = []
    for i in range(3):
        # Get the Google Places API place ID for each recommendation
        place_id = get_place_id(api_key, restaurant_name=names[i], area=areas[i])
        place_details = get_place_details(api_key, place_id=place_id)

        # Append full Google Places API response to results
        results.append({
            "name": names[i],
            "similarity": similarities[i],
            "area": areas[i],
            "place_id": place_id,
            "place_details": place_details  # Include full Google Places API response as is
        })

    first_place_details = results[0]['place_details']
    cust_reviews = extract_reviews(first_place_details)
    review_summary = small_reviews_summary(cust_reviews)
    print(review_summary)
    classify = classify_text(review_summary["text"])
    print(classify)
    print(type(classify))

    classification_result = classify_text(review_summary["text"])


    # Access the sentiment attribute using dot notation
    sentiment_value = classification_result.sentiment

    return JSONResponse(content={
        "first_place_summary": review_summary["text"],
        "first_place_classification": sentiment_value,
        "top_3_recommendations": results
    })


@app.post("/find_similar/")
async def find_similar(img: UploadFile = File(...)):
    """Find similar images based on the uploaded file."""
    temp_file_path = f"temp_{img.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await img.read())

    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    # Find similar images
    similar_images = find_similar_images(temp_file_path, image_features, df_output, model, n_similar=3)
    print(f"Found {len(similar_images)} similar images.")
    # Clean up the temporary file
    os.remove(temp_file_path)
    results = []
    for sim_score, sim_img in similar_images:
        print(f"Processing image: {sim_img}")
        row = df_output[df_output['IMG_FILE'] == sim_img]
        if not row.empty:
            row = row.iloc[0]
            place_id = row.get('place_id')
            # Check if place_id is valid
            if pd.notna(place_id):
                print(f"Using existing place_id: {place_id}")
                place_details = get_place_details(api_key,place_id)
            else:
                restaurant_name = row['name']
                print(f"Original Name: {restaurant_name}")
                # Clean and separate name and area
                cleaned_name, area = separate_name_area(restaurant_name)
                print(f"Trying to find place_id for: Name='{cleaned_name}', Area='{area}'")
                if cleaned_name and area:
                    place_id = get_place_id(api_key, restaurant_name=cleaned_name, area=area)
                else:
                    print("Warning: Cleaned name or area is empty.")
                    place_id = None

                if pd.notna(place_id):
                    print(f"Found place_id: {place_id}")
                    place_details = get_place_details(api_key,place_id)
                else:
                    print(f"Warning: No valid place_id found for restaurant '{cleaned_name}'.")

            restaurant = row['name']
            results.append({
                "name": restaurant,
                "similarity": sim_score,
                "image url": row['photo_url'],
                "place_details": place_details
            })
        else:
            print(f"Warning: Image '{sim_img}' not found in the output images DataFrame.")


    first_place_details = results[0]['place_details']
    cust_reviews = extract_reviews(first_place_details)
    review_summary = small_reviews_summary(cust_reviews)
    print(review_summary)
    classify = classify_text(review_summary["text"])
    print(classify)
    print(type(classify))

    classification_result = classify_text(review_summary["text"])


    # Access the sentiment attribute using dot notation
    sentiment_value = classification_result.sentiment
   # return JSONResponse(content={"similar_images": results})
    return JSONResponse(content={
        "first_place_summary": review_summary["text"],
        "first_place_classification": sentiment_value,
        "top_3_recommendations": results
    })

@app.get("/")
def root():
    """Root endpoint for greeting."""
    return {'greeting': 'Hello'}
