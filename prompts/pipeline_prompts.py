import json
from typing import List
from data.components import ValidComponent, load_components
from models.models import Example, Strategy, find_valid_component_by_name
from prompts.examples import example_1, example_2, example_3


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
        formatted_examples += f"""
        description: {description}
        strategy: {
            Strategy(
                ChainOfThought=script_model.ChainOfThought,
                Components=[c.Name for c in script_model.Components]
            ).model_dump_json()
        }
        """ + "\n\n"
    return formatted_examples


grasshopper_script_model_system_template = """
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
""".format(EXAMPLES=format_script_examples([example_1, example_2, example_3]))


description_template = """
description: {DESCRIPTION}
"""


strategy_system_template = """
You are a Grasshopper3d Expert and are going to help create a Grasshopper
definition.
You will be given a description of the script to create.
- First, you must provide a concise and well defined strategy for how to
approach the grasshopper script.
- Next provide a list of the essential components required to execute the
strategy.

<examples>
{EXAMPLES}
</examples>
""".format(EXAMPLES=format_strategy_examples(
    [example_1, example_2, example_3]
))


follow_up_system_template = """
You are a Grasshopper3d Expert and are going to help create a Grasshopper
definition.
You will be given the following:
- Description of the script to create
- A strategy for creating the script
- Some potential components to be used in the script

<examples>
{EXAMPLES}
</examples>
""".format(EXAMPLES=format_script_examples(
    [example_1, example_2, example_3]
))


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
            name=c,
            errors=[]
        )
        for c in strategy.Components]
    components_str = ''
    for c in components:
        components_str += c.model_dump_json()

    return """
    Description: {DESCRIPTION}
    ===
    Strategy: {STRATEGY}
    ===
    Components: {COMPONENTS}
    """.format(
        DESCRIPTION=description,
        STRATEGY=strategy_str,
        COMPONENTS=components_str
    )
