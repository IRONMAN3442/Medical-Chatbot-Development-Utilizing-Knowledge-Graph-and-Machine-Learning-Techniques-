# import json

# # Replace 'your_file.json' with the path to your JSON file
# file_path = 'data/medlineplus.json'

# # Load the JSON data
# with open(file_path, 'r',encoding="utf8") as file:
#     data = json.load(file)

# # If your JSON data is a list of objects
# if isinstance(data, list):
#     for obj in data:
#         print(obj.keys())

# # If your JSON data is a single object
# elif isinstance(data, dict):
#     print(data.keys())

# # If it's something else, you might need to handle that specifically
# else:
#     print("Data is neither a list of objects nor a single object.")


from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "grammar_model")

args = TTSettings(num_beams=5, min_length=1)

# Add the prefix "grammar: " before each input 
result = happy_tt.generate_text("grammar: This sentences has has bads grammar.", args=args)

print(result.text) # This sentence has bad grammar.
