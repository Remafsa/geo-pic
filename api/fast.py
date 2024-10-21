from fastapi import FastAPI, File, UploadFile, HTTPException

from fastapi.responses import JSONResponse
import os
import pandas as pd
from dotenv import load_dotenv
from recommendation_system.ml_logic import find_similar_images
from recommendation_system.ml_logic import print_similar_images  # Adjust the import based on your package structure
# from tensorflow.keras.applications import ResNet50
from content_based_recommender.content_based_recommendations import *
from scripts import *

load_dotenv()

api_key = "AIzaSyC3Q5AmIGUahFzX5oEuViaZRpOgZ4OzP2s"
# os.getenv('API_KEY')

app = FastAPI()


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


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
# # Load the existing image features from the CSV
# csv_path = 'notebooks/image_features.csv'
# df = pd.read_csv(csv_path)
# sub_df = df.iloc[:, :2048]
# # Optionally, reset the index if needed
# sub_df.reset_index(drop=True, inplace=True)
# # Assuming 'IMG_FILE' contains the paths and features are in subsequent columns
# image_features = df.iloc[:, 1:].values  # Adjust based on your CSV structure
# local_image_paths = df['IMG_FILE'].tolist()
# @app.post("/find_similar/")
# async def find_similar(file: UploadFile = File(...)):
#     # Save the uploaded file temporarily
#     temp_file_path = f"temp_{file.filename}"
#     with open(temp_file_path, "wb") as f:
#         f.write(await file.read())
#     # Find similar images using your existing function
#     similar_images = find_similar_images(temp_file_path, image_features, df, model, n_similar=10)
# #q
#     # Clean up the temporary file
#     os.remove(temp_file_path)
#     # Prepare the results using the print_similar_images logic
#     results = []
#     for sim_score, sim_img in similar_images:
#         row = df[df['IMG_FILE'] == sim_img].iloc[0]
#         result = {
#             "image_path": sim_img,
#             "name": row['name'],
#             "image_url": row['photo_url'],
#             "cosine_similarity": sim_score
#         }
#         results.append(result)
#     return JSONResponse(content={"similar_images": results})


@app.get("/")
def root():
    return {'greeting': 'Hello'}
