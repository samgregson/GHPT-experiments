import json
import os

# Get the absolute path of the components.json file
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'components.json'))

# Load the components.json file to a dictionary variable
def load_components():
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'components.json'), 'r') as f:
        components_dict = json.load(f)
    return components_dict