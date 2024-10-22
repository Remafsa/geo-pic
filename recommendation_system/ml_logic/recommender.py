
import numpy as np
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.applications.resnet50 import preprocess_input
from recommendation_system.ml_logic.feature_extractor import extract_features

def recommend_similar_images(input_image_path, image_features, image_urls, model, top_n=5):
    img = image_utils.load_img(input_image_path, target_size=(224, 224))
    img_data = image_utils.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    input_features = model.predict(img_data).flatten().reshape(1, -1)

    knn = NearestNeighbors(n_neighbors=top_n, metric='euclidean')
    knn.fit(image_features)
    distances, indices = knn.kneighbors(input_features)

    recommended_images = [image_urls[idx] for idx in indices.flatten()]
    return recommended_images
import pandas as pd

def find_cosine_similarity(source_features, test_features):
    dot_product = np.dot(source_features, test_features)
    source_norm = np.linalg.norm(source_features)
    test_norm = np.linalg.norm(test_features)
    if source_norm == 0 or test_norm == 0:
        return 0.0  # Handle case where one of the vectors is zero
    return dot_product / (source_norm * test_norm)
def find_similar_images(target_image_path, image_features, downloaded_df, model, n_similar=3):
    """
    Find similar images based on cosine similarity of their features.

    Parameters:
    - target_image_path: str, path to the target image.
    - image_features: np.ndarray, feature vectors for the dataset images.
    - downloaded_df: pd.DataFrame, DataFrame containing image metadata including URLs and local paths.
    - model: pre-trained model used for extracting features.
    - n_similar: int, number of similar images to return.

    Returns:
    - List of tuples containing (similarity score, local image path).
    """
    # Extract features of the target image
    target_features = extract_features([target_image_path], model, csv_save_path="", make_csv=False)
    if target_features.size == 0:
        return []

    # Calculate cosine similarity between the target and all dataset images
    similarities = []
    for idx, features in enumerate(image_features):
        cosine_similarity = find_cosine_similarity(target_features[0], features)
        local_image_path = downloaded_df.iloc[idx]['IMG_FILE']
        restaurant_name = downloaded_df.iloc[idx]['name']

        # Store cosine similarity, image path, and restaurant name
        similarities.append((cosine_similarity, local_image_path, restaurant_name))

    # Sort images by similarity in descending order
    similarities.sort(reverse=True, key=lambda x: x[0])

    # Set to track unique restaurant names and their corresponding images
    unique_restaurants = set()
    unique_similar_images = []

    for cosine_similarity, local_image_path, restaurant_name in similarities:
        if restaurant_name not in unique_restaurants:
            unique_restaurants.add(restaurant_name)  # Add restaurant to the set
            unique_similar_images.append((cosine_similarity, local_image_path))  # Add to results

        # Stop if we have enough unique images
        if len(unique_similar_images) >= n_similar:
            break

    return unique_similar_images

def print_similar_images(similar_images, downloaded_df):
    """
    Print details of the similar images.

    Parameters:
    - similar_images: list of tuples, where each tuple contains (similarity score, image path).
    - downloaded_df: pd.DataFrame, DataFrame containing image metadata including URLs and local paths.
    """
    for sim_score, sim_img in similar_images:
        row = downloaded_df[downloaded_df['IMG_FILE'] == sim_img].iloc[0]

        name = row['name']  # Restaurant name
        image_url = row['photo_url']  # Image URL
        # Uncomment to include additional details
        # google_id = row['google_id']  # Google ID
        # place_id = row['place_id']  # Place ID
        # location_link = row['location_link']  # Location link
        # latitude = row['latitude']  # Latitude
        # longitude = row['longitude']  # Longitude
        # photo_date = row['photo_date']  # Photo date

        print(
            f"Image Path: {sim_img}, "
            f"Name: {name}, "
            f"Image URL: {image_url}, "
            # f"Google ID: {google_id}, "
            # f"Place ID: {place_id}, "
            # f"Location Link: {location_link}, "
            # f"Latitude: {latitude}, "
            # f"Longitude: {longitude}, "
            # f"Photo Date: {photo_date}, "
            f"Cosine Similarity: {sim_score:.4f}"
        )
