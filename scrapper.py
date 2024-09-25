from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time


# Set up Selenium WebDriver using ChromeDriverManager
def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# Function to search for a disease using Selenium and return the product page URLs
def search_disease(driver, disease):
    driver.get('https://www.1mg.com/')
    time.sleep(2)

    # Locate search bar and input the disease name
    search_bar = driver.find_element(By.ID, 'srchBarShwInfo')
    search_bar.clear()
    search_bar.send_keys(disease)
    search_bar.submit()

    time.sleep(3)  # Allow time for the page to load

    return driver.page_source


# Function to extract product links from the search results page using BeautifulSoup
def extract_product_links(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract all product links
    product_links = []

    for a_tag in soup.find_all('a', class_='style__product-link___1hWpa'):
        link = a_tag.get('href')
        if link.startswith('/'):
            link = f"https://www.1mg.com{link}"  # Convert relative to absolute URL
        if link not in product_links:  # Avoid duplicate links
            product_links.append(link)

    return product_links


# Function to extract product details
def extract_product_details(driver, product_url):
    driver.get(product_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_data = {}

    # Extract product name
    name = soup.find('h1', class_='ProductTitle__product-title___2aHk7')
    if name:
        product_data['name'] = name.get_text().strip()

    # Extract product description
    description = soup.find('div', class_='ProductDescription__description-content___A_qCZ')
    if description:
        product_data['description'] = description.get_text(separator="\n").strip()

    return product_data


# Main process
def main():
    driver = setup_driver()
    diseases = [
        "Common cold",
        "Sinusitis",
        "Whooping Cough",
        "Respiratory Syncytial Virus",
        "Allergic Rhinitis",
        "COVID-19",
        "Dengue Fever",
        "Rheumatic Fever",
        "Influenza"
    ]

    all_product_data = []

    for disease in diseases:
        # Search for the disease and extract product links
        page_source = search_disease(driver, disease)
        product_links = extract_product_links(page_source)


        # Extract and store details for each product
        product_counter = 1
        for product_link in product_links:
            print(f"Extracting data for {product_link}:")
            product_details = extract_product_details(driver, product_link)
            product_id = f"{disease}_{product_counter}"
            product_counter += 1
            all_product_data.append({"id": product_id, "url": product_link, "data": product_details})

    driver.quit()

    # Save output as JSON file
    with open("indian_meds.json", "w") as json_file:
        json.dump(all_product_data, json_file, indent=4)


if __name__ == "__main__":
    main()
