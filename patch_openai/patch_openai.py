from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai.types import CreateEmbeddingResponse
from typing_extensions import Union, overload, ParamSpec
from functools import wraps
import inspect
import requests
from typing import Callable, Any

T_ParamSpec = ParamSpec("T_ParamSpec")
load_dotenv()

@overload
def patch_openai(client: OpenAI) -> OpenAI: ...


@overload
def patch_openai(client: AsyncOpenAI) -> AsyncOpenAI: ...


def patch_openai(
    client: Union[OpenAI, AsyncOpenAI]
) -> Union[OpenAI, AsyncOpenAI]:
    """
    Patch the `client.chat.completions.create` method

    Enables the following features:

    - The OpenAI request is sent to a custom FastAPI server
    """
    api_key = client.api_key

    def is_async(func: Callable[..., Any]) -> bool:
        """
        Returns true if the callable is async, accounting for wrapped
        callables
        """
        is_coroutine = inspect.iscoroutinefunction(func)
        while hasattr(func, "__wrapped__"):
            func = func.__wrapped__  # type: ignore - dynamic
            is_coroutine = is_coroutine or inspect.iscoroutinefunction(func)
        return is_coroutine

    # Chat Completions:
    chat_func = client.chat.completions.create
    chat_func_is_async = is_async(chat_func)

    def call_chat(*args, **kwargs):
        body = {"kwargs": kwargs, "base_url": str(client.base_url)}
        request_url = "https://fastapi-production-e161.up.railway.app/chat"

        headers = {
            "api_key": api_key
        }

        response = requests.post(url=request_url, json=body, headers=headers)

        # Create a ChatCompletion object from the dictionary
        chat_completion = ChatCompletion.model_validate_json(response.content)

        return chat_completion

    @wraps(chat_func)
    async def new_create_async(*args, **kwargs):
        response = call_chat(*args, **kwargs)
        return response

    @wraps(chat_func)
    def new_create_sync(*args, **kwargs):
        response = call_chat(*args, **kwargs)
        return response

    new_create = new_create_async if chat_func_is_async else new_create_sync

    # Embeddings:
    embeddings_func = client.embeddings.create
    embeddings_func_is_async = is_async(embeddings_func)

    def call_embeddings(*args, **kwargs):
        body = {"kwargs": kwargs, "base_url": str(client.base_url)}
        request_url = "https://fastapi-production-e161.up.railway.app/embeddings"

        headers = {
            "api_key": api_key
        }

        response = requests.post(url=request_url, json=body, headers=headers)

        # Create a ChatCompletion object from the dictionary
        embedding_response = CreateEmbeddingResponse.model_validate_json(response.content)

        return embedding_response

    @wraps(chat_func)
    async def new_embeddings_async(*args, **kwargs):
        response = call_embeddings(*args, **kwargs)
        return response

    @wraps(chat_func)
    def new_embeddings_sync(*args, **kwargs):
        response = call_embeddings(*args, **kwargs)
        return response

    new_embeddings = new_embeddings_async if embeddings_func_is_async else new_embeddings_sync

    client.chat.completions.create = new_create
    client.embeddings.create = new_embeddings

    return client
