import numpy as np
from PIL import Image
from scipy.spatial.distance import cosine

def calculate_image_similarity(image1, image2):
    """
    Calculates the similarity between two images using the Euclidean distance between their pixel values.

    Parameters:
    - image1 (numpy.ndarray): First image as a NumPy array.
    - image2 (numpy.ndarray): Second image as a NumPy array.

    Returns:
    - float: Similarity score between the two images (0 indicates identical, 1 indicates completely different).
    """
    return np.linalg.norm(image1.flatten() - image2.flatten()) / (image1.shape[0] * image1.shape[1] * 255)

def resize_image(image_path, target_size):
    """
    Resizes an image to the specified target size.

    Parameters:
    - image_path (str): Path to the image file.
    - target_size (tuple): Target size for the image (width, height).

    Returns:
    - numpy.ndarray: Resized image as a NumPy array.
    """
    image = Image.open(image_path)
    image = image.resize(target_size)
    return np.array(image)

def calculate_vector_similarity(vector1, vector2):
    """
    Calculates the cosine similarity between two feature vectors.

    Parameters:
    - vector1 (numpy.ndarray): First feature vector.
    - vector2 (numpy.ndarray): Second feature vector.

    Returns:
    - float: Cosine similarity score between the two vectors (0 indicates orthogonal, 1 indicates identical).
    """
    return 1 - cosine(vector1, vector2)

def get_top_k_indices(similarities, k):
    """
    Returns the indices of the top k largest values in the given similarity list.

    Parameters:
    - similarities (list): List of similarity scores.
    - k (int): Number of top indices to retrieve.

    Returns:
    - list: Indices of the top k largest values in the similarity list.
    """
    return np.argsort(similarities)[:k]
