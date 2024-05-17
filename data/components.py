import json
import os
from pydantic import BaseModel
from typing import List


class InputOutput(BaseModel):
    Name: str
    DataType: str
    IsOptional: bool


class ValidComponent(BaseModel):
    Name: str
    Description: str
    IsCoreComponent: bool
    Inputs: List[InputOutput]
    Outputs: List[InputOutput]


class ValidComponents(BaseModel):
    Components: List[ValidComponent]


# Load the components.json file to a dictionary variable
def load_components() -> ValidComponents:
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'components.json'), 'r') as f:
        components_dict = json.load(f)
    return ValidComponents.model_validate(components_dict)
