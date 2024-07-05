import json
import os
import numpy as np
import openai
from pydantic import BaseModel
from patch_openai.patch_openai import patch_openai
from typing import List, Optional
from models.models import GrasshopperScriptModel


class Example(BaseModel):
    Description: str
    GrasshopperScriptModel: GrasshopperScriptModel
    Embedding: Optional[List[float]] = None


class Examples(BaseModel):
    Examples: List[Example]


def load_examples() -> Examples:
    # file path needed to work with pytest
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'examples.json'), 'r') as f:
        examples_json = json.load(f)
    return Examples.model_validate(examples_json)



def get_examples_with_embeddings() -> Examples:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    example_embeddings_json_path = os.path.join(dir_path, 'examples_embeddings.json')

    if os.path.exists(example_embeddings_json_path):
        # load from example_embeddings.json if file exists
        with open(example_embeddings_json_path, 'r') as f:
            examples_json = json.load(f)
        return Examples.model_validate(examples_json) #this probably doesnt make sense
    else:
        # Generate embeddings for all example names
        examples = load_examples()
        example_desc = [
            f"{e.Description}" for e in examples.Examples
        ]

        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        client = patch_openai(client)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=example_desc,
            encoding_format="float"
        )

        embeddings = [d.embedding for d in response.data]

        for e, embedding in zip(examples.Examples, embeddings):
            e.Embedding = embedding

        # Save embeddings dictionary to JSON file
        with open(example_embeddings_json_path, 'w') as f:
            f.write(examples.model_dump_json())

        return examples


def get_k_nearest_examples(
    k: int,
    query: str,
    examples_with_embeddings: Examples
) -> List[Example]:
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
    for example in examples_with_embeddings.Examples:
        embedding = example.Embedding
        similarity_score: float = cosine_similarity(query_embedding, embedding)
        similarity_scores.append((example, similarity_score))

    # Sort similarity scores in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # Get top k closest matches
    top_k_matches = similarity_scores[:k]

    # Get component names and descriptions for top k matches
    matched_examples: List[Example] = [
        e for e, _ in top_k_matches
    ]
    return matched_examples


