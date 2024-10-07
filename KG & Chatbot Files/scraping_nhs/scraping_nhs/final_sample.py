import requests
from bs4 import BeautifulSoup
import json

# Function to scrape common data
def scrape_common_data(soup):
    article_title = soup.find("h1", {"itemprop": "name"}).text
    article_summary = soup.find("div", {"id": "ency_summary"}).p.text
    alternative_names_section = soup.find("div", {"id": "section-Alt"}).p.text

    return {
        "name": article_title,
        "description": article_summary,
        "alternate_name": alternative_names_section,
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




def save_to_json(data, filename):
    with open(filename, 'a+', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)






# Example usage
url = "https://medlineplus.gov/ency/article/003123.htm"
# url = 'https://medlineplus.gov/ency/article/001592.htm'
# url = 'https://medlineplus.gov/ency/article/003371.htm'
data = scrape_page(url)
if data:
    print("Scraped Data:")
    print(data)
    json_filename = "scraped_data.json"
    save_to_json(data, json_filename)
    print(f"Data saved to {json_filename}")
