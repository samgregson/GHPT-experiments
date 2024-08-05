import os
from typing import List
import openai
from patch_openai.patch_openai import patch_openai


def get_embeddings(text_list: List[str]) -> List[str]:
    """
    Retrieves embeddings for a list of texts using the OpenAI API.

    Args:
        text_list (List[str]): A list of texts for which embeddings need to be
        retrieved.

    Returns:
        List[str]: A list of embeddings corresponding to the input texts.
    """
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    client = patch_openai(client)

    max_tokens = 1000  # limited max_tokens due to vercel timeout
    batches = create_batches(text_list, max_tokens=max_tokens)

    embeddings = []
    for batch in batches:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
            encoding_format="float"
        )
        embeddings.extend([d.embedding for d in response.data])

    return embeddings


def create_batches(
    text_list: List[str],
    max_tokens: int = 8191
) -> List[List[str]]:
    """
    Splits a list of texts into batches based on the maximum number of tokens
    allowed per batch.

    Args:
        text_list (List[str]): A list of texts to be split into batches.
        max_tokens (int, optional): The maximum number of tokens allowed per
        batch. Defaults to 8191.

    Returns:
        List[List[str]]: A list of batches, where each batch is a list of
        texts.

    Example:
        text_list = [
            "This is the first text.",
            "This is the second text.",
            "This is the third text."
        ]
        max_tokens = 10
        create_batches(text_list, max_tokens) -> [
            ["This is the first text.", "This is the second text."],
            ["This is", "the third", "text."]
        ]
    """
    batches = []
    current_batch = []
    current_tokens = 0

    for text in text_list:
        text_tokens = len(text.split())
        if current_tokens + text_tokens <= max_tokens:
            # add to current batch and keep counting
            current_batch.append(text)
            current_tokens += text_tokens
        else:
            # add the batch to batches and start new batch
            batches.append(current_batch)
            current_batch = [text]
            current_tokens = text_tokens

    if current_batch:
        batches.append(current_batch)

    return batches
