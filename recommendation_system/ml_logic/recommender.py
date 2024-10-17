
import numpy as np
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.applications.resnet50 import preprocess_input
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
