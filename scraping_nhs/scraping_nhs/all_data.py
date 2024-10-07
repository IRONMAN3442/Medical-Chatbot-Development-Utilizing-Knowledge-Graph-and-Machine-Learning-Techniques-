import requests
from bs4 import BeautifulSoup
import json
import pymongo
import time

# Function to scrape common data
def scrape_common_data(soup):
    try:
        article_title = soup.find("h1", {"itemprop": "name"}).text
    except AttributeError:
        article_title = "No information"

    alternative_names_section = soup.find("div", {"id": "section-Alt"})
    if alternative_names_section:
        try:
            alternative_names = alternative_names_section.p.text
        except AttributeError:
            alternative_names = "No information"
    else:
        alternative_names = "No information"

    try:
        article_summary = soup.find("div", {"id": "ency_summary"}).p.text
    except AttributeError:
        article_summary = "No information"

    return {
        "name": article_title,
        "description": article_summary,
        "alternate_name": alternative_names,
    }


# Function to scrape sections and their content
def scrape_sections(soup):
    section_data = {}
    section_elements = soup.find_all("div", class_="section")

    for section_element in section_elements:
        section_title_element = section_element.find("h2")
        
        # Check if an h2 element exists for the section title
        if section_title_element:
            section_title = section_title_element.text
        else:
            # If no h2 element is found, you can set a default title or skip the section as needed
            section_title = "No Title Found"
        
        section_content = []

        # Find all paragraphs and list items within the section
        paragraphs = section_element.find_all(["p", "ul", "ol", "li"])
        
        for paragraph in paragraphs:
            section_content.append(paragraph.get_text(strip=True))

        # Store the section content in the section_data dictionary
        section_data[section_title] = section_content

    return section_data


# Function to scrape the entire page
def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the web page for {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape common data
    common_data = scrape_common_data(soup)

    # Scrape sections and their content
    sections = scrape_sections(soup)

    # Create a dictionary with all the data
    scraped_data = {
        **common_data,
        **sections
    }

    return scraped_data
    




def save_to_mongodb(data, collection):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect to localhost
        db = client.get_database("medlineplus")  # Replace with your actual database name
        result = db[collection].insert_one(data)
        print(f"Data inserted with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {str(e)}")

# Access the existing collection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect to localhost
db = client["medlineplus"]
collection = db["disease_names_url"]
count = 0

# Iterate through each document in the collection
for document in collection.find():
    count += 1
    source_url = document.get("source")
    # time.sleep(2)
    if source_url:
        data = scrape_page(source_url)
        if data:
            # Insert the scraped data into a new MongoDB collection
            new_collection_name = "entire_data"  # Replace with your desired collection name
            save_to_mongodb(data, new_collection_name)
            print('Pushed {} disease into new mongo: {}'.format(count, document.get("disease_name")))

# Close the MongoDB client connection
client.close()
