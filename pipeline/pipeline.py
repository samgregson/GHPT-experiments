import textwrap
from typing import List, Union
from instructor import AsyncInstructor, Instructor
import instructor
from langsmith import traceable
from pydantic import BaseModel
from prompts.pipeline_prompts import (
    get_description_strategy_template,
    description_template,
    get_follow_up_system_template,
    get_strategy_system_template,
    problem_statement_system_template,
    strategy_prompt_template
)
from openai.types.chat import ChatCompletion
from models.models import (
    GrasshopperScriptModel,
    ProblemStatement,
    Strategy,
    StrategyRating
)
from data.examples import (
    Example,
    Examples,
    get_examples_with_embeddings,
    get_k_nearest_examples
)
from instructor.retry import InstructorRetryException


@traceable(run_type="retriever")
def pipe_get_examples(user_prompt: str) -> List[Example]:
    input_embedding = get_k_nearest_examples(
        k=3,
        query=user_prompt,
        examples_with_embeddings=get_examples_with_embeddings()
    )
    examples = input_embedding
    return examples


@traceable
async def run_pipeline(
    client: Union[AsyncInstructor, Instructor],
    user_prompt: str
):
    """Runs the LLM program pipeline.

    Args:
        client (Union[AsyncInstructor, Instructor]): The Instructor client.
        user_prompt (str): The user prompt.

    Returns:
        [type]: The completion response.
    """
    model = "gpt-4o-mini"

    examples = pipe_get_examples(
        user_prompt=user_prompt
    )

    problem_statement = await pipe_problem_statement(
        model=model,
        client=client,
        user_prompt=user_prompt
    )

    strategy: Strategy = await pipe_strategy(
        model=model,
        client=client,
        user_prompt=user_prompt,
        problem_statement=problem_statement,
        examples=examples
    )

    response = await pipe_gh_model(
        client,
        user_prompt,
        examples,
        strategy
    )

    return response


@traceable
async def pipe_gh_model(
    client: Union[AsyncInstructor, Instructor],
    user_prompt: str,
    examples: Examples,
    strategy: Strategy,
    model: str = "gpt-4o-mini",
):
    prompt = get_description_strategy_template(
        user_prompt=user_prompt,
        strategy=strategy
    )
    system_prompt = get_follow_up_system_template(examples)

    response = await client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_model=GrasshopperScriptModel,
        max_retries=0
    )

    return response


@traceable
async def pipe_problem_statement(
    client: Union[AsyncInstructor, Instructor],
    user_prompt: str,
    model: str = "gpt-4o-mini"
) -> ProblemStatement:
    prompt = description_template.format(DESCRIPTION=user_prompt)
    system_prompt: str = problem_statement_system_template
    model: str = "gpt-4o-mini"
    temperature: float = 0
    response_model: BaseModel = ProblemStatement
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    response: Strategy = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_model=response_model,
        max_retries=0
    )
    return response


@traceable
async def pipe_strategy(
    client: Union[AsyncInstructor, Instructor],  
    user_prompt: str,
    problem_statement: ProblemStatement,
    examples: List[Example],
    model: str = "gpt-4o-mini"
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

    prompt = strategy_prompt_template.format(
        DESCRIPTION=user_prompt,
        PROBLEM_STATEMENT=problem_statement.model_dump_json()
    )
    system_prompt: str = get_strategy_system_template(examples)
    model: str = "gpt-4o-mini"
    temperature: float = 0
    response_model: BaseModel = Strategy
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    error = False

    response = None
    response_json = None
    try:
        # generate initial strategy
        response: Strategy = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_model=response_model,
            max_retries=0
        )
        response_json = response.model_dump_json()
        # replace 'tool' roles with assistant
        messages[-1] = {"role": "assistant", "content": response_json}
    except InstructorRetryException as e:
        # return the last completion if there is an error
        error = True
        completion: ChatCompletion = e.last_completion
        if client.mode == instructor.Mode.TOOLS:
            response_json = \
                completion.choices[0].message.tool_calls[0].function.arguments
        else:
            response_json = completion.choices[0].message.content

        # replace 'tool' roles with assistant and user
        messages[-2] = {"role": "assistant", "content": response_json}
        messages[-1] = {"role": "user", "content": str(e)}

    # create message history for rating call
    rating_messages = [
        {"role": "system", "content":
         "You are a Grasshopper3d expert. Please rate the strategy."},
        *messages[1:],
        {"role": "user", "content": textwrap.dedent(
            """
            Does the above strategy look correct? Provide the following,
            - input adherance
            - substitution recommendations
            - validity of each step
            - overall score
            """
        )}
    ]
    rating_response: StrategyRating = await client.chat.completions.create(
        model=model,
        messages=rating_messages,
        temperature=temperature,
        response_model=StrategyRating,
        max_retries=0
    )

    # create a new strategy based on feedback
    if rating_response.score < 5 or error is True:
        messages.append({
            "role": "user",
            "content": rating_response.model_dump_json()
        })
        response: ChatCompletion = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_model=response_model,
            max_retries=0
        )

    return response
