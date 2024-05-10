import json

# Load the components.json file to a dictionary variable
with open('../data/components.json', 'r') as f:
    components_dict = json.load(f)
