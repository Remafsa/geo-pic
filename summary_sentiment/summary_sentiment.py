from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
import tiktoken
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo',openai_api_key=OPENAI_API_KEY)
print("LLM gets loaded successfully.")


def extract_reviews(place_details):
    """
    Extracts all review texts from the place details.

    :param place_details: A dictionary containing details about the place, including reviews.
    :return: A list of review texts.
    """
    all_reviews = []
    reviews = place_details.get('reviews', [])

    for review in reviews:
        review_text = review.get('text', 'No review text available')
        all_reviews.append(review_text)
    reviews_str = "".join(each for  each in all_reviews)

    return reviews_str

def small_reviews_summary(cust_reviews: str) -> str:
    summary_statement = """You are an experienced copywriter providing a world-class summary of restaurant reviews {cust_reviews}from numerous diners across various popular review platforms.
    You craft comprehensive summaries that encapsulate the dining experiences shared by a diverse audience, from casual diners to seasoned food critics. Your goal is to distill key insights,
    highlight common themes, and present a balanced view of the restaurant's atmosphere, service, and cuisine, catering to food enthusiasts and everyday patrons alike,
    ensure the following in your summary: Highlight both positive and negative aspects, grouping similar themes together for a smoother flow."""
    summary_prompt = PromptTemplate(input_variables = ["cust_reviews"], template=summary_statement)
    llm_chain = LLMChain(llm=llm, prompt=summary_prompt)
    print(type(cust_reviews))
    review_summary = llm_chain.invoke(cust_reviews)
    # review_summary="Hi"
    return review_summary


# Define the Classification model
class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


# Define a function to classify text
def classify_text(input_text: str) -> Classification:

    # Define the tagging prompt template
    tagging_prompt = ChatPromptTemplate.from_template(
        """
    Extract the desired information from the following passage.

    Only extract the properties mentioned in the 'Classification' function.

    Passage:
    {input}
    """
    )

    # Initialize the LLM with structured output
    llm_structured = ChatOpenAI(temperature=0, model="gpt-3.5-turbo").with_structured_output(
        Classification
    )

    # Create the tagging chain
    tagging_chain = tagging_prompt | llm_structured
    result = tagging_chain.invoke({"input": input_text})

    return result
