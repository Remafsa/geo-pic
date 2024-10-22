import json
import re


def remove_specific_photo_tags(data):
    tags_to_remove = ["drink, food", "food", "other, food", "drink, other, food","people","menu","drink"]

    cleaned_data = [item for item in data if "photo_tags" not in item or item["photo_tags"] not in tags_to_remove]
    return cleaned_data

def separate_name_area(name):
    parts = [part.strip() for part in name.split('-') if part.strip()]
    parts = [part for part in parts if not re.search(r'[\u0600-\u06FF]', part)]
    restaurant_name = ""
    area = ""
    if len(parts) > 0:
        restaurant_name = parts[0]
        if len(parts) > 1:
            area = parts[-1]
    return restaurant_name, area
