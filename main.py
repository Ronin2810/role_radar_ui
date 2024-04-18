import streamlit as st
import PyPDF2
import textract
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.tokenize import word_tokenize
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import http.client
import json

word2vec_model = Word2Vec.load('vectorizer.model')
def calculate_similarity(text1, text2):
    vec1 = np.mean([word2vec_model.wv[word] for word in text1 if word in word2vec_model.wv], axis=0)
    vec2 = np.mean([word2vec_model.wv[word] for word in text2 if word in word2vec_model.wv], axis=0)
    return cosine_similarity([vec1], [vec2])[0][0]

def tokenize_text(text):
    return word_tokenize(text.lower())

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    text = ""
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def preprocess_text(text):
    # Remove bullet points
    text = re.sub(r'\s*[\u2022\u2023\u25E6\u2043\u2219]\s+', ' ', text)
    # Remove unnecessary punctuations, special characters, and newlines
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    resume_tokens = text.split()
    filtered_resume = [word for word in resume_tokens if word.lower() not in stop_words]
    text = ' '.join(filtered_resume)
    return text.strip()

def make_post_request(text):
    # Define the server address and endpoint
    server_address = 'localhost:11434'
    endpoint = '/api/generate'
    # Define the payload
    payload = {
        "model": "mistral",
        "prompt": f"Extract and list only core technologies in the following text:{text} "
    }
    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    try:
        # Create a connection to the server
        connection = http.client.HTTPConnection(server_address)
        # Define request headers
        headers = {'Content-Type': 'application/json'}
        # Send the POST request
        connection.request('POST', endpoint, payload_json, headers)
        # Get the response
        response = connection.getresponse()
        # Print the response status and data
        print("Response status:", response.status)
        print("Response data:")
        response_output = response.read().decode('utf-8').split('\n') 
        json_arr = []
        for i in range(len(response_output)-2):
            json_file = json.loads(response_output[i])
            json_arr.append(json_file)

        output_string = ""
        for json_obj in json_arr:
            output_string+=json_obj["response"]
        print(output_string)
        # Close the connection
        connection.close()
        return output_string
    except Exception as e:
        print("Error:", e)


def make_post_request_new(jd,resume):
    # Define the server address and endpoint
    server_address = 'localhost:11434'
    endpoint = '/api/generate'
    # Define the payload
    payload = {
        "model": "mistral",
        "prompt": f"Two texts will be provided which include the core technologies present in the JD and a resume. List only the technologies that are present in the JD but not in the resume. Here is the JD: {jd}\nHere is the Resume: {resume}"
    }
    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    try:
        # Create a connection to the server
        connection = http.client.HTTPConnection(server_address)
        # Define request headers
        headers = {'Content-Type': 'application/json'}
        # Send the POST request
        connection.request('POST', endpoint, payload_json, headers)
        # Get the response
        response = connection.getresponse()
        # Print the response status and data
        print("Response status:", response.status)
        print("Response data:")
        response_output = response.read().decode('utf-8').split('\n') 
        json_arr = []
        for i in range(len(response_output)-2):
            json_file = json.loads(response_output[i])
            json_arr.append(json_file)

        output_string = ""
        for json_obj in json_arr:
            output_string+=json_obj["response"]
        print(output_string)
        # Close the connection
        connection.close()
        return output_string
    except Exception as e:
        print("Error:", e)






def main():
    st.title("Role Radar")

    # File upload for first PDF
    st.sidebar.title("Upload JD")
    file_1 = st.sidebar.file_uploader("Choose a PDF file", type="pdf",key='jd')

    # File upload for second PDF
    st.sidebar.title("Upload Resume")
    file_2 = st.sidebar.file_uploader("Choose a PDF file", type="pdf",key='resume')

    if file_1 and file_2:
        if st.sidebar.button("Submit"):
            # Extract text from first PDF
            jd = extract_text_from_pdf(file_1)

            # Extract text from second PDF
            profile = extract_text_from_pdf(file_2)

            jd = preprocess_text(jd)
            profile = preprocess_text(profile)
            
            tokenized_jd = tokenize_text(jd)
            tokenized_profile = tokenize_text(profile)
            # Combine text from both PDFs

            # Make prediction
            prediction = calculate_similarity(tokenized_jd, tokenized_profile)
            # prediction = predict_score(jd,profile)
            print("JD:\n",jd)
            print("Resume:\n",profile)
            # Display prediction
            st.success(f"Similarity Score: {prediction*100}%")

            # Fetch Prompt here
            jd_skills = make_post_request(jd)
            st.success(f"SKILLS IN JD\n{jd_skills}")
            resume_skills = make_post_request(profile)
            st.success(f"SKILLS IN RESUME\n{resume_skills}")
            lacking_skills = make_post_request_new(jd_skills,resume_skills)
            st.error(f"SKILLS LACKING IN RESUME:\n{lacking_skills}")


if __name__ == "__main__":
    main()
