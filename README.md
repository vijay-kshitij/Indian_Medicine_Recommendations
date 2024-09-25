# Indian Medicine Recommendation System for Cold-Flu-Fever

[Recommendation Model Link](https://indianmedicinerecommendations.streamlit.app/)

This project is a **LLM-based recommendation system** designed to provide personalized medicine recommendations for common ailments such as colds, flu, and fever. Users can input their symptoms and get medicine recommendations based on data stored in a **ChromaDB vector database**. The application uses Groq's Llama 3.1 model and LangChain for processing and generating recommendations. The database has **306** data points and all the medicines are of the Indian market.

## Technology Stack

- **Python 3.10**
- **Streamlit**: Front-end interface for interacting with the medicine recommender system.
- **Groq's Llama 3.1 Model**: Provides the language model for generating recommendations.
- **ChromaDB**: A vector database used for querying stored medicine data.
- **LangChain**: Used to manage the prompts and LLM chains.
- **Selenium and BeautifulSoup**: For web scraping data related to medicines.


## Project Files

- **`main.py`**: 
   - The main **Streamlit** app file that handles navigation, user input, and displays results.
   - Contains the user interface and sections for About the app, instructions for obtaining the **Groq API key** and the **Recommendation Model**

- **`indian_rec.py`**: 
   - The core logic for handling medicine recommendations.
   - Defines how symptoms are processed and how recommendations are generated using **LangChain** and **ChatGroq**.

- **`scrapper.py`**: 
   - Uses **Selenium** and **BeautifulSoup** to scrape data for medicines from external websites.

- **`data_structuring.py`**: 
   - Structures the scraped data into a **JSON format** containing keys like `name`, `description`, `directions for use`, `id`, and `url`.

- **`vectorDB.py`**: 
   - Handles the storage of structured data in **ChromaDB**, which allows fast and efficient querying of medicine data.

## Important Notes

- The database contains **306 medicines**, so the results may be limited.
- This project is **for demonstration purposes only**. The recommendations provided by the system should not be considered accurate medical advice. Always consult a healthcare professional before making any medical decisions.
- Make sure to **keep your Groq API key secure** and do not share it with anyone.
