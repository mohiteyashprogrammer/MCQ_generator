import os
import sys 
import PyPDF2
import json
import base64 
import streamlit as st 
import traceback
from src.mcqgenerator.logger import  logging



def read_file(file):
    """
    Reads text from a file.
    
    Args:
    - file: A file object
    
    Returns:
    - text: Extracted text from the file
    """

    if file.name.endswith('.pdf'):
        try:
            # If the file is a PDF, use PyPDF2 to extract text from each page
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            logging.info("Error occurred while reading the file")
    

    elif file.name.endswith('.txt'):
        # If the file is a text file, read its contents
        return file.read().decode('utf-8')
    
    else:
        # If the file format is not supported, raise a custom exception
        raise Exception(e)
    

def get_table_data(quiz_str):
    """
    Extracts table data from a quiz string.
    
    Args:
    - quiz_str (str): A string representing the quiz in JSON format
    
    Returns:
    - list: A list of dictionaries containing table data for each MCQ
    """
    try:
        # convert the quiz from a string to a dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq = value["mcq"]
            options = "||".join(
                [
                f"{options}-> {option_value}" for option,option_value in value["options"].items()
                ]
            )

            correct = value["correct"]
            quiz_table_data.append(
                {"MCQ":mcq,
                 "Choice":options,
                 "Correct":correct
                 })
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
    

def set_background(image_file):
    try:
        """
        This function sets the background of a Streamlit app to an image specified by the given image file.

        Parameters:
        image_file (str): The path to the image file to be used as the background.

        Returns:
        None
        """
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{b64_encoded});
             background-size: cover;
            }}
            </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except Exception as e:
        logging.info("Error occurred while setuping background image:")
        raise Exception(e)
    
       
     
