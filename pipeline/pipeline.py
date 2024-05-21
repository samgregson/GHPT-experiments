from typing import Union
from langsmith import traceable
from openai import AsyncOpenAI, OpenAI
from prompts.pipeline_prompts import system_prompt, prompt_template

from models.models import GrasshopperScriptModel


@traceable
async def call_openai_instructor(
    client: Union[OpenAI, AsyncOpenAI],
    prompt: str,
    system_prompt: str = "",
    model: str = "gpt-3.5-turbo-1106",
    temperature: float = 0,
    response_model=GrasshopperScriptModel,
):
    """Calls the OpenAI API to generate a Grasshopper script.

    Args:
        client (Union[OpenAI, AsyncOpenAI]): The OpenAI client.
        prompt (str): The user prompt.
        system_prompt (str, optional): The system prompt.
            Defaults to "".
        model (str, optional): The model to use.
            Defaults to "gpt-3.5-turbo-1106".
        temperature (float, optional): The temperature for text generation.
            Defaults to 0.
        response_model ([type], optional): The response model.
            Defaults to GrasshopperScriptModel.

    Returns:
        [type]: The completion response.
    """
    completion = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_model=response_model,
        max_retries=2
    )

    return completion


@traceable
async def run_pipeline(client: Union[OpenAI, AsyncOpenAI], user_prompt: str):
    """Runs the LLM program pipeline.

    Args:
        client (Union[OpenAI, AsyncOpenAI]): The OpenAI client.
        user_prompt (str): The user prompt.

    Returns:
        [type]: The completion response.
    """

    response = await call_openai_instructor(
        client=client,
        prompt=prompt_template.format(QUESTION=user_prompt),
        system_prompt=system_prompt
    )

    return response
