import json
from collections import defaultdict
import re

def remove_unwanted_characters(text):
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable())
    # Remove special symbols or any other unwanted characters remove "&", "@", and "#"
    text = re.sub(r'[&@#]', '', text)
    return text

def clean_string(s):
    return s.encode('cp1252', errors='ignore').decode('cp1252')

def clean_text(text):
    # If the text is a list, join it into a single string
    if isinstance(text, list):
        text = ' '.join(text)
    # Normalize white space
    text = re.sub(r'\s+', ' ', text)
    # Add space around parentheses (only if there's no space already)
    text = re.sub(r'(?<!\s)(\(|\))', r' \1', text)
    text = re.sub(r'(\(|\))(?!\s)', r'\1 ', text)
    # Replace non-standard quotes with standard quotes
    text = text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    text = text.replace(u"\u201c", '"').replace(u"\u201d", '"')
    # Ensure proper spacing (e.g., "Downwardpalpebral" becomes "Downward palpebral")
    text = ' '.join(re.split(r'([A-Z][a-z]+)', text))
    # Remove unwanted characters
    text = remove_unwanted_characters(text)
    # Remove additional spaces around dashes and other punctuations
    text = re.sub(r'\s*-\s*', '-', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r'\s*\.\s*', '. ', text)
    text = re.sub(r'\s*;\s*', '; ', text)
    text = text.strip()  # Remove leading/trailing whitespace
    return clean_string(text) 




def deduplicate_list(items):
    # Function to deduplicate a list
    seen = set()
    deduped_items = []
    for item in items:
        cleaned_item = clean_text(item)
        cleaned_item = clean_string(cleaned_item)  # Clean the string for encoding
        if cleaned_item not in seen:
            seen.add(cleaned_item)
            deduped_items.append(cleaned_item)
    return deduped_items


def extract_alternate_names(data):
    # Function to extract and deduplicate alternate names
    alt_names = data.get('alternate_name', '').split(';')
    alt_names.extend(data.get('Alternative Names', []))
    return deduplicate_list(alt_names)

def extract_symptoms(data):
    # Function to extract and deduplicate symptoms
    symptoms = data.get('Symptoms', [])
    return deduplicate_list(symptoms)

def clean_data(data):
    # Cleaning and normalizing the data object
    cleaned_data = defaultdict(list)
    # Extracting ID
    cleaned_data['id'] = data.get('_id', {}).get('$oid', '')
    # Cleaning and setting the name
    cleaned_data['name'] = clean_text(data.get('name', ''))
    # Cleaning and setting the description
    cleaned_data['description'] = clean_text(data.get('description', ''))
    # Extracting, cleaning, and deduplicating alternate names
    cleaned_data['alternate_names'] = extract_alternate_names(data)
    # Extracting, cleaning, and deduplicating symptoms
    cleaned_data['symptoms'] = extract_symptoms(data)
    # Cleaning and deduplicating other fields similarly...
    # Assuming other fields follow a similar structure as 'Symptoms' and 'Alternative Names'
    for key in ['Causes', 'Exams and Tests', 'Treatment', 'Support Groups', 'Outlook (Prognosis)', 'Possible Complications', 'When to Contact a Medical Professional', 'Prevention', 'Images', 'References', 'Related MedlinePlus Health Topics']:
        cleaned_data[key.lower().replace(' ', '_')] = deduplicate_list(data.get(key, []))
    # Cleaning 'Review Date' field and renaming it
    review_date = clean_text(data.get('Review Date 11/1/2021', [''])[0])
    cleaned_data['review_date'] = review_date
    return dict(cleaned_data)

file_path = 'data/disease_entries.json'
output_file_path = 'data/disease_cleaned.json'

# Load the JSON data
with open(file_path, 'r', encoding="utf8") as file:
    data = json.load(file)

# Assuming 'data' is a list of records. If it's a single record, wrap it in a list: data = [data]
cleaned_data = [clean_data(record) for record in data]

# Dumping the cleaned data to another file
with open(output_file_path, 'w', encoding="utf8") as file:
    json.dump(cleaned_data, file, indent=2, ensure_ascii=False)
