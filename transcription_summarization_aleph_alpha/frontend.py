"""Frontend Script for the Transcription and Summarization Demo.

Author: Marc Fabian Mezger
Date: March 2023
"""
from pathlib import Path

import streamlit as st
from transcription.api_handler import (  # , summarize_text_using_completion
    ClientWrapper,
    summarize_text_using_summarize,
)
from transcription.transcription_service import transcribe

# create the folder structure
Path("../data/input").mkdir(parents=True, exist_ok=True)
Path("../data/output").mkdir(parents=True, exist_ok=True)

# make a large title
st.title("Transcription and Summarization Demo")


def create_transcripton(file_path: str):
    """Calls the transcription method from the transcribe server, and hands the
    location of the uploaded file over.


    :param file_path: location of the uploaded file.
    :type file_path: str
    """
    text = transcribe(file_name=file_path)
    print(file_path)
    tmp_path = file_path.split(".")[2]
    # join the list to a string
    print(tmp_path)
    tmp_path = tmp_path.split("/")[-1]
    print(tmp_path)
    # save the text to the folder data/output
    with open(f"../data/output/{tmp_path}.txt", "w") as tmp_file:
        tmp_file.write(text)
    st.write("SUCCESS: Transcription was created")
    # return the path to the file
    return text


def summarize(text: str, token: str):
    """This method calls the summarization service from the api handler script.

    :param text: _description_
    :type text: _type_
    :param token: _description_
    :type token: _type_
    """
    # First initialize the Aleph Alpha Connector Client
    if len(token) == 0:
        st.write("ERROR: Please enter a valid Aleph Alpha Token")
    client_wrapper = ClientWrapper(token)

    result = summarize_text_using_summarize(client_wrapper, text)

    # create text box to show the result
    st.text_area("Summarization Result", result, height=500)


# create a  passwort field to upload your aleph alpha token
token = st.text_input("Enter your Aleph Alpha Token", type="password")


# upload a file that can either be mp3 or wav or mp4
uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav", "mp4"])

# save the file to the local directory data input
if uploaded_file is not None:
    with open("../data/input/" + uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())


# initialize a start button if the start button gets called the function transcribe will be called
if st.button("Start"):
    TEXT = create_transcripton("../data/input/" + uploaded_file.name)
    # display the text
    st.text_area("Transcription Result", TEXT, height=500)

    # start the summarization
    summarize(text=TEXT, token=token)
