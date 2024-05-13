import json
import os


# Load the components.json file to a dictionary variable
def load_components():
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'components.json'), 'r') as f:
        components_dict = json.load(f)
    return components_dict