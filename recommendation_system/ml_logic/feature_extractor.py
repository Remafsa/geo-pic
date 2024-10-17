import numpy as np
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.applications.resnet50 import preprocess_input

def extract_features(image_paths,model):
    features = []
    for path in image_paths:
        img = image_utils.load_img(path, target_size=(224, 224))
        img_data = image_utils.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        feature = model.predict(img_data)
        features.append(feature.flatten())
    return np.array(features)
