
from ast import literal_eval
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from fastapi.responses import JSONResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from summary_sentiment.summary_sentiment import *
from scripts import *

import pandas as pd
import sidetable
api_key = os.getenv('API_KEY')

# download nltk packages
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
def process_sentences(text):
    temp_sent =[]
    full_sentence = text
    full_sentence = full_sentence.replace("n't", " not")
    full_sentence = full_sentence.replace("'m", " am")
    full_sentence = full_sentence.replace("'s", " is")
    full_sentence = full_sentence.replace("'re", " are")
    full_sentence = full_sentence.replace("'ll", " will")
    full_sentence = full_sentence.replace("'ve", " have")
    full_sentence = full_sentence.replace("'d", " would")

    # Tokenize words
    words = nltk.word_tokenize(full_sentence)

    # Lemmatize each of the words based on their position in the sentence
    tags = nltk.pos_tag(words)
    for i, word in enumerate(words):
        if tags[i][1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):  # only verbs
            lemmatized = lemmatizer.lemmatize(word, 'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)

        # Remove stop words and non alphabet tokens
        if lemmatized.isalpha():
            temp_sent.append(lemmatized)
    # Some other clean-up
    # full_sentence = ' '.join(temp_sent)

    return ' '.join(temp_sent)

def recommend(description):
    # Convert user input to lowercase
    description = description.lower()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(current_dir, "..", "data", "combined_data.csv")
    data = pd.read_csv(d)

    cities_list = ['amsterdam', 'athens', 'barcelona', 'berlin', 'bratislava',
       'brussels', 'budapest', 'copenhagen', 'dublin', 'edinburgh',
       'geneva', 'hamburg', 'helsinki', 'krakow', 'lisbon', 'ljubljana',
       'london', 'luxembourg', 'lyon', 'madrid', 'milan', 'munich',
       'oporto', 'oslo', 'paris', 'prague', 'rome', 'stockholm', 'vienna',
       'warsaw', 'zurich', 'riyadh', 'jeddah', 'madinah', 'makkah',
       'dammam', 'khobar', 'taif', 'jazan', 'alula', 'al khobar',
       'dhahran']

    # # Extract cities
    cities_input = []
    for city in cities_list:
        if city in description:
            cities_input.append(city)
            description = description.replace(city, "")

    if cities_input:
        data = data[data['city'].isin(cities_input)]

    countries_list = ['netherlands', 'greece', 'spain', 'germany', 'slovakia', 'belgium',
       'hungary', 'denmark', 'ireland', 'scotland', 'switzerland',
       'finland', 'portugal', 'slovenia', 'united kingdom', 'luxembourg',
       'france', 'italy', 'norway', 'czech republic', 'sweden', 'austria',
       'poland']

    # # Same thing for countries
    countries_input = []
    for country in countries_list:
        if country in description:
            countries_input.append(country)
            description = description.replace(country, "")

    if countries_input:
        data = data[data['country'].isin(countries_input)]

    # Process user description text input
    description = process_sentences(description)
    description = description.strip()
    print('Processed user feedback:', description)

    # Init a TF-IDF vectorizer
    tfidfvec = TfidfVectorizer()

    # Fit data on processed reviews
    vec = tfidfvec.fit(data["bag_of_words"])
    features = vec.transform(data["bag_of_words"])

    # Transform user input data based on fitted model
    description_vector =  vec.transform([description])

    # Calculate cosine similarities between users processed input and reviews
    cos_sim = linear_kernel(description_vector, features)

    # Add similarities to data frame
    data['similarity'] = cos_sim[0]

    # Sort data frame by similarities
    data.sort_values(by='similarity', ascending=False, inplace=True)

    return data[['name',"city",'similarity']]

def get_name_recommendation(data):
    # Access the top 3 values of the 'name' column
    return data['name'].iloc[:3].tolist()

def get_city_recommendation(data):
    # Access the top 3 values of the 'city' column
    return data['city'].iloc[:3].tolist()

def get_similarity_recommendation(data):
    # Access the top 3 values of the 'similarity' column
    return data['similarity'].iloc[:3].tolist()
if __name__ == "__main__":

    # Get recommendations based on user input
    recommend_result = recommend("cafe")

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
