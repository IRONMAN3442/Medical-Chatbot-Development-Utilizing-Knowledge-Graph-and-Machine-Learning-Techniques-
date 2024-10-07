import requests
from bs4 import BeautifulSoup

# Define the URL of the page you want to scrape
url = "https://www.nhsinform.scot/illnesses-and-conditions/a-to-z"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print(response.status_code)
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    a_elements = soup.find_all("a", class_="nhs-uk__az-link")

    disease_dict = {}
    disease_names = []
    disease_urls = []
    count=0
    # Iterate through the <a> elements and extract the data
    for a_element in a_elements:
        # Extract the disease name (strip() removes leading/trailing spaces and newline characters)
        disease_name = a_element.text.strip()

        # Extract the URL (prepend the base URL to make it complete)
        base_url = "https://www.nhsinform.scot"
        disease_url = base_url + a_element["href"]

        # Append the extracted data to the respective lists
        disease_names.append(disease_name)
        disease_urls.append(disease_url)

    # Print the extracted data
    for name, url in zip(disease_names, disease_urls):
        temp_dict={}
        print(f"Disease Name: {name}")
        print(f"Disease URL: {url}")
        temp_dict[name] = name
        temp_dict[name] = url
        disease_dict[count] = temp_dict
        count+=1
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
print(count)
print(disease_dict)