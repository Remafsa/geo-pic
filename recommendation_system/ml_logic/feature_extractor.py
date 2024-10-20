import numpy as np
import csv
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.applications.resnet50 import preprocess_input

def extract_features(image_paths, model, csv_save_path="",make_csv=False):
    """
    Extract features from images and save them to a CSV file.

    Parameters:
    - image_paths: list of str, paths to the images.
    - model: Keras model used for feature extraction.
    - csv_save_path: str, path where the CSV file will be saved.

    Returns:
    - np.ndarray, array of extracted features.
    """
    features = []

    # Extract features for each image
    for path in image_paths:
        img = image_utils.load_img(path, target_size=(224, 224))
        img_data = image_utils.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        feature = model.predict(img_data)
        features.append(feature.flatten())

    features_array = np.array(features)

    # Save features to a CSV file
    if make_csv:
        with open(csv_save_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header (column names)
            header = ['File Path'] + [f'Feature_{i+1}' for i in range(features_array.shape[1])]
            writer.writerow(header)

            # Write each feature row with the corresponding image path
            for idx, feature in enumerate(features_array):
                writer.writerow([image_paths[idx]] + feature.tolist())

        print(f"Features saved to {csv_save_path}")

    return features_array
