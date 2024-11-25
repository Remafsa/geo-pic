import streamlit as st
import requests
import tempfile
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
# Google Places API functions
def get_place_ids(api_key, restaurant_name, area=""):
    query = f"{restaurant_name} {area}".strip()
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    response = requests.get(search_url)
    results = response.json().get('results', [])
    return [result.get('place_id') for result in results[:3]]  # Get top 3 place IDs
def get_place_details(api_key, place_id):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(details_url)
    return response.json().get('result', {})
# Function to create place card
def create_place_card(col, image_url, place_name, location, rating, review_count, rating_label, place_url, bg_color="#f0f0f5"):
    with col:
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:10px; border-radius:10px; height:500px; display:flex; flex-direction:column; justify-content:space-between;">
                <img src="{image_url}" style="width:100%; height:200px; object-fit:cover; border-radius:10px;">
                <div style="margin-top:10px;">
                    <h4 style="margin:0;">{place_name}</h4>
                    <p style="color:gray; font-size:14px; margin:0;">📍 {location}</p>
                    <p style="font-size:14px; margin:0;">
                        <a href="{place_url}" target="_blank">View on Google Maps</a>
                    </p>
                </div>
                <div style="display:flex; align-items:center; justify-content:space-between; margin-top:10px;">
                    <div style="background-color:#4CAF50; color:white; padding:4px 8px; border-radius:5px; text-align:center;">
                        {rating}
                    </div>
                    <div style="margin-left:10px;">
                        <p style="color:green; font-size:16px; margin:0;">{rating_label}</p>
                        <p style="color:gray; font-size:12px; margin:0;">({review_count} Reviews)</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# Function to create sentiment emoji
def get_sentiment_emoji(sentiment_label):
    if sentiment_label == "positive":
        return "😊"  # Happy emoji for positive sentiment
    elif sentiment_label == "mixed":
        return "😐"  # Neutral face for mixed sentiment
    elif sentiment_label == "negative":
        return "😔"  # Sad face for negative sentiment
    else:
        return "🤔"  # Thinking face for unknown sentiment
# Function to display sentiment creatively
def display_sentiment(sentiment_label, sentiment_score):
    emoji = get_sentiment_emoji(sentiment_label)
    # Background color based on sentiment
    bg_color = "#D4EDDA" if sentiment_label == "positive" else "#FFF3CD" if sentiment_label == "neutral" else "#F8D7DA"
    text_color = "#155724" if sentiment_label == "positive" else "#856404" if sentiment_label == "neutral" else "#721C24"
    # Display sentiment creatively with emoji and colored card
    st.markdown(
        f"""
        <div style="background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;">
            <h3 style="color:{text_color};">Sentiment: {sentiment_label.capitalize()}</h3>
            <div style="font-size:50px;">{emoji}</div>
            <p style="color:{text_color}; font-size:18px;">Score: {sentiment_score:.4f}</p>
        </div>
        """, unsafe_allow_html=True
    )
    # Add a progress bar to visually show the sentiment score
    sentiment_normalized = (sentiment_score + 1) / 2  # Normalize to 0-1 range if score is between -1 to 1
    # st.progress(f"similarity {sentiment_normalized}")

# Sidebar with radio options
st.sidebar.header("Options")
option = st.sidebar.radio("Choose one of the options:", ["Upload image", "Descriptive text writing"])

# Initialize the variables for restaurant recommendations
first_place_summary = ""
classification = ""
top_recommendation = []

# Section for uploading an image
if option == "Upload image":
    st.header("Upload an Image")
    uploaded_image = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_image.read())
            temp_file_path = temp_file.name

        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        st.write("Processing the image for recommendations...")

        # Call the API for image-based recommendations
        YOUR_API_URL = "http://localhost:8000/find_similar/"
        with st.spinner('loading...'):
        # Send the POST request with the image file
            files = {'img': open(temp_file_path, 'rb')}  # Use the correct field name expected by FastAPI
            response = requests.post(YOUR_API_URL, files=files)

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            # Access the data from the API response

            first_place_summary = data.get('first_place_summary', 'No summary available')
            similarity = data.get('similarity', 'No similarity available')
            classification = data.get('first_place_classification', 'No classification available')
            top_recommendation = data.get('top_3_recommendations', [])
            # st.write(top_recommendation)

        else:
            st.write("Error fetching recommendations from the API.")

# Section for descriptive text writing
elif option == "Descriptive text writing":
    st.header("Enter a Descriptive Text")
    description_text = st.text_area("Enter the description of the place or restaurant here:")

    # Analyze button for text input
    if st.button("Analyze"):
        if description_text:
            st.write(f"Searching based on the description: {description_text}")

            # Call the API for text-based recommendations
            YOUR_API_URL = "http://localhost:8000/recommendation/"

            # Send the description text as a query parameter
            params = {
                'user_input': description_text  # Use the expected key for your API
            }

            response = requests.get(YOUR_API_URL, params=params)  # Use GET method with query parameters

            if response.status_code == 200:
                data = response.json()  # Parse the JSON response

                # Access the data from the API response
                first_place_summary = data.get('first_place_summary', 'No summary available')
                classification = data.get('first_place_classification', 'No classification available')
                similarity = data.get('similarity', 'No similarity available')
                top_recommendation = data.get('top_3_recommendations', [])
                # st.write(top_recommendation)

# Display the top 3 restaurants based on uploaded image or description
if top_recommendation:
    st.write("### Recommended Places")
    columns = st.columns(3)

    for i, recommendation in enumerate(top_recommendation[:3]):  # Limit to top 3
        place_details = recommendation.get("place_details", {})


        # Extract relevant data for display
        place_name = recommendation.get('name', 'Unknown')
        location = place_details.get('adr_address', 'Unknown location')
        rating = place_details.get('rating', 'N/A')
        review_count = place_details.get('user_ratings_total', '0')
        place_url = place_details.get('url', 'https://maps.google.com')
        similarity = recommendation.get('similarity', 'No similarity score available')

        # Image handling
        # image_url = recommendation.get('image url', 'https://via.placeholder.com/400')
        photo_reference = place_details.get('photos', [{}])[0].get('photo_reference', '')
        image_url = (
                f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
                if photo_reference else "https://via.placeholder.com/400"
            )

        create_place_card(
                columns[i],  # Use the correct column based on index
                image_url=image_url,
                place_name=place_name,
                location=location,
                rating=str(rating),
                review_count=str(review_count),
                rating_label="Good" if isinstance(rating, float) and rating > 4 else "Average",
                place_url=place_url
            )

        # Create place card using dynamic data in the respective column
        # columns[i].image(image_url, caption=place_name, use_column_width=True)
        # columns[i].write(f"Location: {location}")
        # columns[i].write(f"Rating: {rating} ({review_count} reviews)")
        # columns[i].write(f"[Visit Website]({place_url})")


if first_place_summary:
    st.write("### Summary:")
    st.write(first_place_summary)

if classification:
    st.write("### Sentiment Analysis:")
    display_sentiment(classification, similarity)


# if top_recommendation:
#     st.write("### Recommended Places")
#     columns = st.columns(3)
#     for i, (restaurant_name, area) in enumerate(top_recommendation[:3]):  # Limit to top 3
#          place_details = recommendation.get("place_details", {})

#         for place_id in place_details:
#             place_details = top_recommendation
#             if place_details:
#                 # Extract relevant data for display
#                 place_name = place_details.get('name', 'Unknown')
#                 location = place_details.get('formatted_address', 'Unknown location')
#                 rating = place_details.get('rating', 'N/A')
#                 review_count = place_details.get('user_ratings_total', '0')
#                 place_url = place_details.get('url', 'https://maps.google.com')  # Extracting the URL
#                 # Get the image URL
#                 photo_reference = place_details.get('photos', [{}])[0].get('photo_reference', '')
#                 image_url = (
#                     f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
#                     if photo_reference else "https://via.placeholder.com/400"
#                 )
#                 # Create place card using dynamic data in the respective column
#                 create_place_card(
#                     columns[i],  # Use the correct column based on index
#                     image_url=image_url,
#                     place_name=place_name,
#                     location=location,
#                     rating=str(rating),
#                     review_count=str(review_count),
#                     rating_label="Good" if isinstance(rating, float) and rating > 4 else "Average",
#                     place_url=place_url
#                 )
#                 break  # Break after processing the first place_id

# # Display the summary and sentiment
# if first_place_summary:
#     st.write("### Summary:")
#     st.write(first_place_summary)

# if classification:
#     st.write("### Sentiment Analysis:")
#     display_sentiment(classification, similarity)



# # st.sidebar.header("Options")
# # option = st.sidebar.radio("Choose one of the options:", ["Upload image", "Descriptive text writing"])
# # # Initialize the restaurants variable


# # # Section for uploading an image
# # if option == "Upload image":
# #     YOUR_API_URL = "http://localhost:8000/find_similar/"
# #     response = requests.get(YOUR_API_URL)
# #     if response.status_code == 200:
# #         data = response.json()  # Parse the JSON response
# #     st.header("Upload an Image")
# #     uploaded_image = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
# #     if uploaded_image:
# #         st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
# #         st.write("Processing the image for recommendations...")
# #         # Simulate restaurant recommendations for testing

# #         first_place_summary = data['first_place_summary']
# #         classification = data['first_place_classification']
# #         top_recommendation = data['top_3_recommendations']

# # # Section for descriptive text writing
# # elif option == "Descriptive text writing":
# #     YOUR_API_URL = "http://localhost:8000/recommendation/"
# #     response = requests.get(YOUR_API_URL)
# #     if response.status_code == 200:
# #         data = response.json()  # Parse the JSON response
# #     st.header("Enter a Descriptive Text")
# #     description_text = st.text_area("Enter the description of the place or restaurant here:")
# #     # Analyze button for text input
# #     if st.button("Analyze"):
# #         if description_text:
# #             st.write(f"Searching based on the description: {description_text}")
# #             # Simulated response data for summary and sentiment
# #             # You can replace this with actual data from your API
# #             first_place_summary = data['first_place_summary']
# #             classification = data['first_place_classification']
# #             top_recommendation = data['top_3_recommendations']

# # # Display the top 3 restaurants based on uploaded image or description
# # if top_recommendation:
# #     st.write("### Recommended Places")
# #     columns = st.columns(3)
# #     for i, (restaurant_name, area) in enumerate(top_recommendation[:3]):  # Limit to top 3
# #         place_ids = get_place_ids(API_KEY, restaurant_name, area)
# #         for place_id in place_ids:
# #             place_details = top_recommendation
# #             if place_details:
# #                 # Extract relevant data for display
# #                 place_name = place_details.get('name', 'Unknown')
# #                 location = place_details.get('formatted_address', 'Unknown location')
# #                 rating = place_details.get('rating', 'N/A')
# #                 review_count = place_details.get('user_ratings_total', '0')
# #                 place_url = place_details.get('url', 'https://maps.google.com')  # Extracting the URL
# #                 # Get the image URL
# #                 photo_reference = place_details.get('photos', [{}])[0].get('photo_reference', '')
# #                 image_url = (
# #                     f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
# #                     if photo_reference else "https://via.placeholder.com/400"
# #                 )
# #                 # Create place card using dynamic data in the respective column
# #                 create_place_card(
# #                     columns[i],  # Use the correct column based on index
# #                     image_url=image_url,
# #                     place_name=place_name,
# #                     location=location,
# #                     rating=str(rating),
# #                     review_count=str(review_count),
# #                     rating_label="Good" if isinstance(rating, float) and rating > 4 else "Average",
# #                     place_url=place_url
# #                 )
# #                 break  # Break after processing the first place_id
# #     # Extract and display the summary and sentiment after displaying images
# #     summary = first_place_summary.get('summary', 'No summary available')
# #     sentiment = classification.get('sentiment', 'No sentiment data available')
# #     # Get sentiment label and score
# #     sentiment_label = sentiment['label']
# #     sentiment_score = sentiment['score']
# #     # Display the summary
# #     st.write("### Summary:")
# #     st.write(summary)
# #     # Display the sentiment creatively
# #     st.write("### Sentiment Analysis:")
# #     display_sentiment(sentiment_label, sentiment_score)
