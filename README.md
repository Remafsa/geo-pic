
# Geo-pic

Geo-pic is a project designed to simplify your search experience by providing seamless, personalized recommendations. With an integrated approach using machine learning, APIs, and sentiment analysis, Geo-pic finds the perfect match for your needs. Whether you're looking for specific locations, images, or related content, Geo-pic ensures you receive tailored results.

## Features

- **Simplified Search**: Enter prompts to quickly retrieve relevant information.
- **Image Analysis**: Process images using ResNet50 to identify content and retrieve matching data.
- **Personalized Recommendations**: Receive tailored suggestions based on sentiment analysis and user preferences.
- **API Integrations**: Utilize Google APIs for accurate data retrieval.
- **Summary and Sentiment Analysis**: Summarize and analyze the results for refined recommendations.

## How It Works

1. **Prompt Processing**: User inputs are processed with Natural Language Toolkit (NLTK) and machine learning models to identify keywords and relevant data.
2. **Image Analysis**: Images are processed through ResNet50 to identify objects, locations, or themes.
3. **Data Retrieval**: Google APIs are used to fetch relevant information based on the processed inputs.
4. **Sentiment Analysis**: Data is analyzed to ensure recommendations match the user's intended mood or preference.
5. **Summary and Recommendation**: A summary is generated, and recommendations are provided through FastAPI, enhancing the user experience with a list of images or locations.

## Built With

- **Python**: Core language used for implementing machine learning models and API interactions.
- **NLTK**: For processing text prompts.
- **ResNet50**: Deep learning model for image classification.
- **Google APIs**: For data retrieval.
- **OpenAI**: For summarization.
- **FastAPI**: Framework to deploy recommendations.

## Getting Started

### Prerequisites

- Python 
- Necessary libraries installed (NLTK, FastAPI, etc.)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Remafsa/geo-pic.git
    ```
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Example

To get a recommendation:
- Submit a prompt like `"I’m looking for a romantic restaurant in Jeddah with a view of the sea."`
- Or upload an image of a cafe.

Geo-pic will analyze the input and suggest relevant images or locations that match your interest.

