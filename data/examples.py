import json
import os
from models.models import Examples

def load_examples() -> Examples:
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'examples.json'), 'r') as f:
        examples_json = json.load(f)
    return Examples.model_validate(examples_json)



