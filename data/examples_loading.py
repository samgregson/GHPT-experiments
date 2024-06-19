import json
from typing import List
from pydantic import BaseModel #this should not be needed here, this will get cleaned up when its moved to its own examples.py
import os
from models.models import Example

class Examples(BaseModel): #do we need BaseModel? What does it do? 
    Examples: List[Example]

# Load the components.json file to a dictionary variable
def load_examples() -> Examples:
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'examples.json'), 'r') as f:
        examples_json = json.load(f)
    return Examples.model_validate(examples_json)



