import requests
from bs4 import BeautifulSoup

# Define the URL of the web page
url = "https://medlineplus.gov/ency/article/003123.htm"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the article title (Abdominal bloating)
    article_title = soup.find("h1", {"itemprop": "name"}).text

    # Extract the article summary (Abdominal bloating description)
    article_summary = soup.find("div", {"id": "ency_summary"}).p.text

    # Extract the causes section
    causes_section = soup.find("div", {"id": "section-1"})
    causes = [li.text for li in causes_section.find_all("li")]

    # Extract the home care section
    home_care_section = soup.find("div", {"id": "section-2"})
    home_care_steps = [li.text for li in home_care_section.find_all("li")]

    # Extract the "When to Contact a Medical Professional" section
    contact_professional_section = soup.find("div", {"id": "section-3"})
    contact_professional_list = [li.text for li in contact_professional_section.find_all("li")]

    # Extract the alternative names section
    alternative_names_section = soup.find("div", {"id": "section-Alt"})
    alternative_names = alternative_names_section.p.text

    # Print or process the extracted data as needed
    print("Article Title:", article_title)
    print('========================================')
    print("Article Summary:", article_summary)
    print('========================================')
    print("Causes:", causes)
    print('========================================')
    print("Home Care Steps:", home_care_steps)
    print('========================================')
    print("When to Contact a Medical Professional:", contact_professional_list)
    print('========================================')
    print("Alternative Names:", alternative_names)
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
