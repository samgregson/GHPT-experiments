import textwrap
from typing import List, Optional, Union
from instructor import AsyncInstructor, Instructor
from langsmith import traceable
from pydantic import BaseModel, Field
from prompts.pipeline_prompts import (
    get_description_strategy_template,
    description_template,
    follow_up_system_template,
    strategy_system_template
)
from openai.types.chat import ChatCompletion
from models.models import GrasshopperScriptModel, Strategy, StrategyRating
from instructor.retry import InstructorRetryException


@traceable
async def call_openai_instructor(
    client: Union[AsyncInstructor, Instructor],  # Union[OpenAI, AsyncOpenAI],
    prompt: str,
    system_prompt: str = "",
    model: str = "gpt-3.5-turbo-1106",
    temperature: float = 0,
    response_model: BaseModel = GrasshopperScriptModel,
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
        max_retries=0
    )

    return completion


@traceable
async def run_pipeline(
    client: Union[AsyncInstructor, Instructor],  # Union[OpenAI, AsyncOpenAI],
    user_prompt: str
):
    """Runs the LLM program pipeline.

    Args:
        client (Union[AsyncInstructor, Instructor]): The Instructor client.
        user_prompt (str): The user prompt.

    Returns:
        [type]: The completion response.
    """

    strategy: Strategy = await pipe_strategy(
        client=client,
        user_prompt=user_prompt
    )

    response = await call_openai_instructor(
        client=client,
        prompt=get_description_strategy_template(
            user_prompt=user_prompt,
            strategy=strategy
        ),
        system_prompt=follow_up_system_template
    )

    return response
    # return strategy


@traceable
async def pipe_strategy(
    client: Union[AsyncInstructor, Instructor],  # Union[OpenAI, AsyncOpenAI],
    user_prompt: str,
) -> Strategy:
    """
    Generates a strategy based on the given user prompt.

    Args:
        client (Union[AsyncInstructor, Instructor]): The OpenAI client used
        for generating the strategy.
        user_prompt (str): The user prompt description of the script.

    Returns:
        Strategy: The generated strategy.

    Raises:
        InstructorRetryException: If there is an error during the strategy
        generation process.

    """

    prompt = description_template.format(DESCRIPTION=user_prompt)
    system_prompt: str = strategy_system_template
    model: str = "gpt-3.5-turbo-1106"
    temperature: float = 0
    response_model: BaseModel = Strategy
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    error = False

    # generate initial strategy
    try:
        response: Strategy = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_model=response_model,
            max_retries=0
        )
    # return the last completion if there is an error
    except InstructorRetryException as e:
        error = True
        completion: ChatCompletion = e.last_completion
        response = completion.choices[0].message

    # create message history for rating call
    rating_messages = [
        {"role": "system", "content":
         "You are a Grasshopper3d expert. Please rate the strategy."},
        *messages[1:],
        {"role": "user", "content":
         "Does the above strategy look correct? Answer with a single number "
         "from 0 to 10 with no preamble. Where 0 is not at all and 10 is "
         "perfect."}
    ]
    rating_response: StrategyRating = await client.chat.completions.create(
        model=model,
        messages=rating_messages,
        temperature=temperature,
        response_model=StrategyRating,
        max_retries=0
    )

    # create a new strategy based on feedback
    if rating_response.value < 5 or error is True:
        messages.append({
            "role": "user", "content": rating_response.reasoning +
            ", ".join(rating_response.susbstitution_recommendations)
        })
        response: ChatCompletion = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_model=response_model,
            max_retries=0
        )

    return response
