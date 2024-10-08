import json
import textwrap
from typing import List
from data.components import ValidComponent, load_components
from models.models import Strategy, find_valid_component_by_name
from data.examples import Example, Examples


def format_script_examples(examples: list[str]) -> str:
    """
    formats a list of examples, as json strings, extracting description
    and gh script model reasoning
    """
    formatted_examples = ""
    for example in examples:
        example_model = Example.model_validate(json.loads(example))
        description = example_model.Description
        scriptModel = example_model.GrasshopperScriptModel
        formatted_examples += f"""
        description: {description}
        scriptModel: {scriptModel.model_dump_json()}
        """ + "\n\n"
    return formatted_examples


def format_strategy_examples(examples: list[str]) -> str:
    """
    formats a list of examples, as json strings, extracting description
    and cot reasoning
    """
    formatted_examples = ""
    for example in examples:
        example_model = Example.model_validate(json.loads(example))
        description = example_model.Description
        script_model = example_model.GrasshopperScriptModel
        formatted_examples += textwrap.dedent(f"""
        # Description
        {description}
        # Strategy
        {script_model.ChainOfThought}
        {str([c.Name for c in script_model.Components])}
        """) + "\n\n"
    return formatted_examples


def get_grasshopper_script_model_system_template(examples: Examples) -> str:
    grasshopper_script_model_system_template = textwrap.dedent("""
    You are a Grasshopper3d Expert and are going to help create a Grasshopper
    definition.
    You will be given a description of the script to create.
    Keep the answers short and concise.
    Make sure you create and connect a component for every non-optional input

    Always use the given format, avoid any devitation.

    ===

    Here are some examples of expected output

    <examples>
    {EXAMPLES}
    </examples>

    ===

    """).format(EXAMPLES=format_script_examples(
        [e.model_dump_json() for e in examples]
    ))

    return grasshopper_script_model_system_template


description_template = textwrap.dedent("""
# Description
{DESCRIPTION}
""")

strategy_prompt_template = textwrap.dedent("""
# Description
{DESCRIPTION}

# Problem Statement
{PROBLEM_STATEMENT}
""")

problem_statement_system_template = textwrap.dedent("""
You are a Grasshopper3d Expert and are going to help create a Grasshopper
definition.
""")


def get_strategy_system_template(examples: Examples) -> str:
    strategy_system_template = textwrap.dedent("""
    You are a Grasshopper3d Expert and are going to help create a Grasshopper
    definition
    You will be given a description of the script to create, required input and
    output, and you may also be given some feedback and advice

    Make sure you follow the expected inputs and outputs.
    If any advice is provided make sure you consider this carefully in defining
    your strategy.

    - First, you must provide a concise and well defined strategy for how to
    approach the grasshopper script.
    - Next provide a list of the essential components required to execute the
    strategy.


    <examples>
    {EXAMPLES}
    </examples>
    """).format(EXAMPLES=format_strategy_examples(
        [e.model_dump_json() for e in examples]
    ))

    return strategy_system_template
 

def get_follow_up_system_template(examples: Examples) -> str:
    follow_up_system_template = textwrap.dedent("""
    You are a Grasshopper3d Expert and are going to help create a Grasshopper
    definition.
    You will be given the following:
    - Description of the script to create
    - A strategy for creating the script
    - Some potential components to be used in the script

    <examples>
    {EXAMPLES}
    </examples>
    """).format(EXAMPLES=format_script_examples(
        [e.model_dump_json() for e in examples]
    ))

    return follow_up_system_template


valid_components = load_components()


def get_description_strategy_template(user_prompt: str, strategy: Strategy):
    '''
    Template for Description, Strategy, Component (details)
    To be used for generating the grasshopper script.
    '''
    description = user_prompt
    strategy_str = strategy.ChainOfThought
    components: List[ValidComponent] = \
        [find_valid_component_by_name(
            valid_components=valid_components,
            name=c.ComponentName,
            errors=[]
        )
        for c in strategy.ChainOfThought]
    components_str = ''
    for c in components:
        components_str += c.model_dump_json()

    return textwrap.dedent("""
    # Description
    {DESCRIPTION}
    ===
    # Strategy
    {STRATEGY}
    ===
    # Components
    {COMPONENTS}
    """).format(
        DESCRIPTION=description,
        STRATEGY=strategy_str,
        COMPONENTS=components_str
    )
