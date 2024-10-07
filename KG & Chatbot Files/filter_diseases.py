import json

file_path = 'data/medlineplus.json'

# Load the JSON data
with open(file_path, 'r',encoding="utf8") as file:
    data = json.load(file)

# Define the keys that must all be present for disease entries
required_disease_keys = {'Causes', 'Symptoms', 'Treatment', 'Outlook (Prognosis)'}

# Function to check if an entry is related to a disease
def is_disease_entry(entry):
    return all(key in entry for key in required_disease_keys)

# Filter out the disease-related entries
disease_entries = [entry for entry in data if is_disease_entry(entry)]

# Do something with the filtered disease entries
# For example, print them or save them to a file
for disease in disease_entries:
    print(disease)

# If you want to save the filtered entries to a file
with open('data/disease_entries.json', 'w') as outfile:
    json.dump(disease_entries, outfile, indent=4)
