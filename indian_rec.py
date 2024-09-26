import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
# from dotenv import load_dotenv
from vectorDB import collection
import json
import ast


# load_dotenv()


# Predefined symptoms
symptoms_list = [
    "Fever", "Cough", "Dry Cough", "Productive (Mucus-Producing) Cough",
    "Runny or Stuffy Nose", "Sneezing", "Sore Throat", "Headache",
    "Fatigue or Weakness", "Body Aches or Muscle Pain", "Shortness of Breath or Difficulty Breathing",
    "Loss of Taste or Smell", "Chest Congestion", "Watery or Itchy Eyes"
]


# Function to create a prompt for the LLM
def generate_prompt(symptoms, results):
    prompt_template = PromptTemplate.from_template(
        """
        You are an expert medicine recommender specialized in respiratory diseases such as cold, flu, fever, and other related minor ailments.
        Given the following symptoms: {symptoms}, recommend medicines from the data stored in the vector database only, including dosage and URLs.
        {results}

        The only output I want is a list of dictionary with the recommended medicines Name, URL and dosage.
        Nothing else. If you are creating something else too and the dictionary name with vector database or something else,
        then just output that dictionary/vector database. I want nothing else. No function, no method of telling how it's gonna be done.
        The final output would be a list of dictionary with each element of the list is a dictionary having keys: Name, url and dosage.
        Moreover, if there's any typos (like spelling mistake) then correct it. And I want different results ,i.e, no 2
        results would have the same Medicine Name.

        Important:
        1. Ensure that each medicine name is unique. If there are multiple URLs for the same medicine (due to different quantities or packaging sizes), then only return the first one.
        2. For each medicine, only include one URL, preferably the one with the most common or standard quantity.
        3. Correct any typos, and ensure no duplicate entries based on the medicine name.
        4. No preamble or additional information. Just return the list of dictionaries with unique medicines.


        I know you will do an amazing job with this. Good Luck!
        Please avoid any preamble.
        ### NO PREAMBLE
        """
    )
    return prompt_template



# Function to retrieve medicines from ChromaDB
def get_medicines_from_chromadb(symptoms, llm):
    # Create the prompt using the provided symptoms
    results = collection.query(query_texts=symptoms, n_results=3).get('metadatas', [])

    prompt = generate_prompt(symptoms, results)

    # Create an LLMChain with the LLM and prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Invoke the chain to generate a response
    llm_response = llm_chain.run({"symptoms": symptoms, "results": results})

    return llm_response


# Create a function to be called in another script
def run_indian_meds_recommender(groq_api_key):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=0
    )

    st.title("Medicine Recommender for Cold-Flu-Fever")
    st.write("Get personalized medicine recommendations based on your symptoms")

    # Option for user input: Search bar and symptom selection
    selected_symptoms = st.multiselect(
        "Select your symptoms from the list below",
        symptoms_list
    )

    search_input = st.text_input("Type any other details: eg. Ayurvedic, Homeopathy, Syrup.....")


    # Combine search and selected symptoms
    if search_input:
        symptoms = search_input
    elif selected_symptoms:
        symptoms = ', '.join(selected_symptoms)
    else:
        symptoms = None


    # Button to trigger the search
    if st.button("Get Medicine Recommendations"):
        if symptoms:
            st.write(f"Searching for medicines")

            medicines = get_medicines_from_chromadb(symptoms, llm)

            # Convert string with single quotes into a Python object (list of dictionaries)
            python_obj = ast.literal_eval(medicines)

            # Now convert the Python object to a proper JSON formatted string
            json_response = json.dumps(python_obj)

            # If you need it as a Python object (list of dictionaries), you can do:
            medicines = json.loads(json_response)

            if medicines:
                st.write("Here are some recommended medicines:")
                for i, med in enumerate(medicines, 1):
                    # st.write(f"{i}. Medicine: {med['Name']} \n URL: {med['url']} \n Dosage: {med['dosage']}")
                    st.markdown(
                        f"{i}. **Medicine:** {med['Name']} <br> **URL:** {med['url']} <br> **Dosage:** {med['dosage']}",
                        unsafe_allow_html=True)

            else:
                st.write("No medicines found for the given symptoms.")
        else:
            st.write("Please provide some symptoms to search.")





