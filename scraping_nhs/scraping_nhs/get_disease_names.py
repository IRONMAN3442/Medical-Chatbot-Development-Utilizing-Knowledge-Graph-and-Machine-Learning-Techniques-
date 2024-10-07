from pymongo.mongo_client import MongoClient
import requests
from bs4 import BeautifulSoup


# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
client = MongoClient("mongodb://localhost:27017/")

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Create or select a database and a collection within that database to store your data
    db = client["medlineplus"]
    collection = db["disease_names_url"]

    count = 0

    for x in range(65, 91):
        x = chr(x)
        url = 'https://medlineplus.gov/ency/encyclopedia_' + x + '.htm'
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        link_elements = soup.find('ul', id='index').find_all('a')

        # Initialize an empty list to store the disease information
        disease_info_list = []

        for link in link_elements:
            url = 'https://medlineplus.gov/ency/' + link['href']
            if 'article' in url:
                count += 1
                name = link.get_text()
                disease_info = {'disease_name': name, 'source': url}
                disease_info_list.append(disease_info)
                # Print the disease details as they are scraped
                print(f"URL: {url}")
                print(f"Name: {name}")
                print()

        # Print the number of diseases scraped from the current page
        print(f"Scraped {len(disease_info_list)} diseases from {x} page.")
        

        # Insert the scraped disease information into the MongoDB collection
        collection.insert_many(disease_info_list)

    print(f"Total {count} diseases scraped and stored in the MongoDB collection.")

except Exception as e:
    print(e)
