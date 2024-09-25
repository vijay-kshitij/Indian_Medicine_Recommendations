from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import json
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),  # Replace with your actual Groq API key
    temperature=0
)

# Load the JSON file
with open("indian_meds.json", "r") as f:
    df = json.load(f)


# Prompt to extract and structure data
prompt_extract = PromptTemplate.from_template("""
You are given a product description where various sections are embedded within the text. Your task is to extract and structure the information into distinct fields. The description contains the following sections:

Here is the input description:
{description}

1. Product Name: The first part of the description, starting from the beginning until the first \\n (newline).
2. Description: The content between the Product Name and the Key Ingredients section.
3. Key Ingredients: This section begins after the text \\nKey Ingredients:\\n and ends before the next section. Within the section replace \\n with a comma.
4. Key Benefits: This section starts after \\nKey Benefits:\\n and ends before the next section. Within the section replace \\n with a comma.
5. Directions for Use: This section begins after \\nDirections for Use:\\n and ends before the next section. Within the section replace \\n with a comma.
6. Safety Information: This section starts after \\nSafety Information:\\n and continues until the end of the description or until another section is reached. Within the section replace \\n with a comma.

Your task is to extract and format the data into the following JSON structure:
{{
  "name": "Extracted Product Name",
  "description": "Extracted Description",
  "Directions for Use": "Extracted Directions for Use",
}}

No need to return Key Ingredients, Key benefits, Safety Information. Only the ones which are mentioned above in the JSON structure

Only return the valid JSON. No code or method of doing the process.
### VALID JSON (NO PREAMBLE):
"""
)

modified_data = []

for product in df:
    description = product["data"].get("description", "")

    chain_extract = prompt_extract | llm

    response = chain_extract.invoke(input={'description': description})

    json_parser = JsonOutputParser()
    json_res = json_parser.parse(response.content)

    # Create the final structure
    json_res["id"] = product["id"]
    json_res["url"] = product["url"]

    modified_data.append(json_res)

# Save the modified data to a new file
with open("modified_indian_meds.json", "w") as f:
    json.dump(modified_data, f, indent=4)

print("Data extraction complete and saved to modified_indian_meds.json.")