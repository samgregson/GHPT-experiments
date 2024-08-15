import json
import os
import numpy as np
import openai
from pydantic import BaseModel
from typing import List, Optional
from data.get_embeddings import get_embeddings
from patch_openai.patch_openai import patch_openai


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
    Embedding: Optional[List[float]] = None


class ValidComponents(BaseModel):
    Components: List[ValidComponent]


# Load the components.json file to a dictionary variable
def load_components() -> ValidComponents:
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'components.json'), 'r') as f:
        components_json = json.load(f)
    return ValidComponents.model_validate(components_json)


def get_components_with_embeddings() -> ValidComponents:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    embeddings_json_path = os.path.join(dir_path, 'embeddings.json')

    if os.path.exists(embeddings_json_path):
        # load from embeddings.json if file exists
        with open(embeddings_json_path, 'r') as f:
            components_json = json.load(f)
            return ValidComponents.model_validate(components_json)

    else:
        # Generate embeddings for all components
        valid_components = load_components()
        component_text = [
            f"{c.Name}: ({c.Description})" for c in valid_components.Components
        ]

        embeddings = get_embeddings(text_list=component_text)

        for c, embedding in zip(valid_components.Components, embeddings):
            c.Embedding = embedding

        # Save embeddings dictionary to JSON file
        with open(embeddings_json_path, 'w') as f:
            f.write(valid_components.model_dump_json())

        return valid_components


def get_k_nearest_components(
    k: int,
    query: str,
    valid_components_with_embeddings: ValidComponents
):
    """
    Uses OpenAI Embeddings API to get the k closest matches to an input string
    """

    # Generate embedding for query
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    client = patch_openai(client)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query,
        encoding_format="float"
    )

    query_embedding = response.data[0].embedding

    # Calculate similarity scores between query embedding and component
    # embeddings
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    similarity_scores = []
    for component in valid_components_with_embeddings.Components:
        embedding = component.Embedding
        similarity_score: float = cosine_similarity(query_embedding, embedding)
        similarity_scores.append((component, similarity_score))

    # Sort similarity scores in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # Get top k closest matches
    top_k_matches = similarity_scores[:k]

    # Get component names and descriptions for top k matches
    matched_components: List[ValidComponent] = [
        c for c, _ in top_k_matches
    ]
    return [f"'{c.Name}' ({c.Description})" for c in matched_components]
