from ml_logic import download_images, extract_features, recommend_similar_images,extract_image_urls_from_json
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model

# Load image URLs from JSON or another source
image_urls = extract_image_urls_from_json("Outscraper-20241011183106xs96_fine_dining_restaurant.json")
 # Replace with your logic to load URLs

# Download images
local_image_paths = download_images(image_urls)


base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)
# Extract features
image_features = extract_features(local_image_paths)

# Recommend similar images
input_image_path = "/home/mohammed/code/Remafsa/geo-pic/recommendation_system/افضل-مطعم-فخم-في-الرياض.webp"
recommended_images = recommend_similar_images(input_image_path, image_features, image_urls, model)
print("Recommended Similar Images:")
for img in recommended_images:
    print(img)
