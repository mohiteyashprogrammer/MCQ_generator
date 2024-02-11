import streamlit as st
import json
import traceback
import os
import sys
import pandas as pd
from src.mcqgenerator.logger import logging
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.utils import read_file,get_table_data,set_background


#loading json file
with open('C:\\Users\\yash mohite\\OneDrive\\Desktop\\MCQ_generator\\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

# set backgtound
set_background("C:\\Users\\yash mohite\\OneDrive\\Desktop\\MCQ_generator\\OIP.jpg")

# Creating a Title For APP
st.title("MCQ Generator Application WITH OPENAI And LangChain")

# Create a Form Using st.form
with st.form("user_input"):
        # uplode file
        uploded_file = st.file_uploader("Uplode a PDF or TXT File")

        # Input Field 
        mcq_count = st.number_input("Number of MCQs",min_value=3,max_value=100)

        #Subject field
        subject = st.text_input("Insert Subject",max_chars=25)

        # Quiz Tone Field
        tone  = st.text_input("Complexity Level Of Questions",max_chars=20,placeholder="Simple")

        #Add Button
        button = st.form_submit_button("Create MCQs")

        # Check if the button is clicked and all fields have input

        if button and uploded_file is not None and mcq_count and subject and tone:
            with st.spinner("Loading..."):
                try:
                    text = read_file(uploded_file)
                    #count tokens and the cost of Api requests
                    with get_openai_callback() as cb:
                        response=generate_evaluate_chain(
                            {
                                "text": text,
                                "number": mcq_count,
                                "subject":subject,
                                "tone": tone,
                                "response_json": json.dumps(RESPONSE_JSON)
                            }
                        )

                except Exception as e:
                    traceback.print_exception(type(e),e,e.__traceback__)
                    st.error("Error")

                else:
                    print(f"Total Tokens:{cb.total_tokens}")
                    print(f"Prompt Tokens:{cb.prompt_tokens}")
                    print(f"Completing Tokens:{cb.completion_tokens}")
                    print(f"Total Cost:{cb.total_cost}")

                    if isinstance(response,dict):

                        # Extract the quiz data from response
                        quiz = response.get('quiz',None)
                        if quiz  is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index = df.index+1
                                st.table(df)
                                # Display the review in the text box as well
                                st.text_area(label="Review",value=response["review"])
                            else:
                                st.error("Error in the Table Data")


                    else:
                        st.write(response)

                

                                








