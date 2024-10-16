import json

with open('<JSON file>', 'r', encoding='utf-8') as file:
    data = json.load(file)

def remove_specific_photo_tags(data):
    tags_to_remove = ["drink, food", "food", "other, food", "drink, other, food","people","menu","drink"]

    cleaned_data = [item for item in data if "photo_tags" not in item or item["photo_tags"] not in tags_to_remove]
    return cleaned_data


cleaned_data = remove_specific_photo_tags(data)


with open('full_data_cleaned_without_food_people.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

print("new file")
