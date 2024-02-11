# Import all Imp Packages
import openai
import langchain
import os
import sys
import json
import pandas
import traceback
import dotenv
import PyPDF2
from src.mcqgenerator.logger import  logging
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

# Load the environment variables from the .env file
dotenv.load_dotenv()

# Access the environment variables just like you would with os.environ
key = os.getenv("OPENAI_API_KEY")

try:
    # Setting up a ChatGPT instance
    llm = ChatOpenAI(
        # Providing your OpenAI API key
        openai_api_key = key,
        # Specifying the model you want to use. Here, you're using "gpt-3.5-turbo".
        model_name = "gpt-3.5-turbo",
        # Setting the temperature parameter to 1.0. Temperature controls the randomness of the model's responses.
        temperature = 1.0,
    )  
except Exception as e:
    logging.info("Error occurred while Setting up a ChatGPT instance")
    raise Exception(e)


# Define a template string for generating a quiz
template = """
Text:{text}
You are an expert MCQ maker.Given the about text, it is your job to\
create a quize of {number} multiple choice questions fro {subject} students in {tone} tone.
Make sure the questions are not repated and check all questions to be conforming the text as well.
Make sure to Format your Response like RESPONSE_JSON below use it as guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

try:
    # Define a PromptTemplate for generating prompts
    quiz_generator_prompt = PromptTemplate(

        # Define input variables that will be used in the template
        input_variables = ["text", "number", "subject", "tone", "response_json"],

        # Provide the template string defined earlier
        template = template
    )
except Exception as e:
    logging.info("Error occurred while Setting up a PromptTemplate instance")
    raise Exception(e)

try:
    # Create an LLMChain instance for generating quizzes
    quiz_chain = LLMChain(

        # Provide the ChatGPT instance initialized earlier
        llm=llm,
        # Provide the prompt template for generating quiz prompts
        prompt=quiz_generator_prompt,
        # Specify the key for accessing the output related to quizzes
        output_key="quiz",
        # Enable verbose mode to receive additional information during generation
        verbose=True
    )
except Exception as e:
    logging.info("Error occurred while Setting up a LLMChain instance")
    raise Exception(e)

# Define a PromptTemplate for generating review prompts
template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

try:

    # Define a PromptTemplate for evaluating quizzes
    quiz_evaluation_prompt = PromptTemplate(
        # Define input variables that will be used in the template
        input_variables=["subject", "quiz"],
        # Provide the template string defined elsewhere (not provided in this snippet)
        template=template2
    )
except Exception as e:
    logging.info("Error occurred while Setting up a  Evaluation PromptTemplate instance")
    raise Exception(e)

try:
    # Create an LLMChain instance for evaluating quizzes
    review_chain = LLMChain(
        # Provide the ChatGPT instance initialized earlier
        llm=llm,
        # Provide the prompt template for evaluating quizzes
        prompt=quiz_evaluation_prompt,
        # Specify the key for accessing the output related to quiz evaluations
        output_key="review",
        # Enable verbose mode to receive additional information during evaluation
        verbose=True
    )

except Exception as e:
    logging.info("Error occurred while Setting up a  Evaluation LLMChain instance")
    raise Exception(e)

try:
    # Create a SequentialChain instance to combine quiz generation and evaluation
    generate_evaluate_chain = SequentialChain(
        # Specify the individual chains to be executed sequentially
        chains=[quiz_chain, review_chain],
        # Define input variables expected by the combined chain
        input_variables=["text", "number", "subject", "tone", "response_json"],
        # Define output variables produced by the combined chain
        output_variables=["quiz", "review"],
        verbose=True
    )
except Exception as e:
    logging.info("Error occurred while Setting up a SequentialChain instance")
    raise Exception(e)