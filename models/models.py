import textwrap
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator
)
from typing import List, Literal, Optional, Union
from pydantic_core import InitErrorDetails, PydanticCustomError
from data.components import (
    ValidComponents,
    get_components_with_embeddings,
    get_k_nearest_components,
    ValidComponent
)

valid_components = get_components_with_embeddings()


class ComponentNames(BaseModel):
    Name: str = Field(
        ...,
        description="The name of the component to be added. Only standard "
                    "grasshopper components are allowed"
    )

    @field_validator("Name")
    @classmethod
    def validate_name_exists(cls, v):
        name_iterator = (component.Name for component in
                         valid_components.Components)
        if v not in name_iterator:
            raise ValueError(f"The component {v} could not be found, either "
                             "there is a typo or it does not exist. Please "
                             "choose a valid component.")
        return v


class AbstractComponentWithId(ComponentNames):
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )


class Component(AbstractComponentWithId):
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )


class NumberSlider(AbstractComponentWithId):
    Name: Literal["Number Slider"]
    Value: str = Field(
        None,
        alias='Value',
        description="The range of values for the Number Slider. "
                    "In the format '<start>..<default>..<end>'. "
                    "Give a decent range of values to allow for flexibility"
    )


class Panel(AbstractComponentWithId):
    Name: Literal["Panel"]
    Value: str = Field(
        None,
        alias='Value',
        description="The text for the Panel Component. "
                    "In the format '<text>'"
    )


class Point(AbstractComponentWithId):
    Name: Literal["Point"]
    Value: str = Field(
        None,
        alias='Value',
        description="The 3D coordinates for the Point Component. "
                    "In the format '<x>,<y>,<z>'"
    )


class InputConnectionDetail(BaseModel):
    Id: int = Field(
        ...,
        description="The unique identifier of the component the connection is "
                    "related to"
    )
    ParameterName: str = Field(
        ...,
        description="The specific input parameter of the component that the "
                    "connection affects"
    )


class OutputConnectionDetail(BaseModel):
    Id: int = Field(
        ...,
        description="The unique identifier of the component the connection is "
                    "related to"
        )
    ParameterName: str = Field(
        ...,
        description="The specific output parameter of the component that the "
                    "connection affects"
        )


class Connection(BaseModel):
    From: OutputConnectionDetail = Field(
        ...,
        description="The source component and parameter from which the "
                    "connection originates"
    )
    To: InputConnectionDetail = Field(
        ...,
        description="The target component and parameter that the connection "
                    "is directing to"
    )


class StrategyStep(BaseModel):
    StepDescription: str
    ComponentName: str


class Strategy(BaseModel):
    """
    Detailed and concise Strategy for creating a grasshopper script
    """
    ChainOfThought: List[StrategyStep] = Field(
        ...,
        description=textwrap.dedent(
            """
            step by step plan explaining how the script will
            acheive the aim, including the all components used.
            Start by defining all inputs, e.g. sliders, points, or panels
            Be specific, avoid making vague statements.
            This strategy needs to give specific instructions that can easily
            be carried out by a novice grasshopper user, without the need to
            infer any details
            """
        )
    )

    @field_validator("ChainOfThought")
    @classmethod
    def validate_components_exist(cls, v):
        errors: List[InitErrorDetails] = []
        c: StrategyStep
        for c in v:
            name_list = [component.Name
                         for component in valid_components.Components]
            if c.ComponentName not in name_list \
               and \
               c.ComponentName not in ['Number Slider', 'Panel', 'Point']:
                errors.append(InitErrorDetails(
                    type=PydanticCustomError(
                        "",
                        textwrap.dedent(f"""
                        The component '{c.ComponentName}' could not be found,
                        either there is a typo or it does not exist.
                        Did you mean any of these: {get_k_nearest_components(
                            k=5,
                            query=f'${c.ComponentName}: ${c.StepDescription}',
                            valid_components_with_embeddings=valid_components
                        )}?
                        Substitute the component for the actual
                        component that you require only if they are equivalent!
                        If no equivalent component is found consider redefining
                        the strategy and 'ChainOfThought' from scratch!
                        """)
                    )
                ))
        if len(errors) > 0:
            raise ValidationError.from_exception_data(
                title='Components',
                line_errors=errors,
            )
        return v


class GrasshopperScriptModel(BaseModel):
    """
    A acyclic directed graph representation of a grasshopper script with all
    grasshopper components and the connections between them.
    Use Number Slider for variable inputs to the script
    """
    ChainOfThought: str = Field(
        ...,
        description="step by step rational explaining how the script acheives "
                    "the aim, including the main components used"
    )
    Components: List[Union[NumberSlider, Panel, Point, Component]] = Field(
        ...,
        description="A list of components to be added to the configuration"
    )
    Connections: List[Connection] = Field(
        ...,
        description="A list of connections defining relationships between "
                    "components' parameters"
    )
    Advice: str = Field(
        ...,
        description="A piece of advice or instruction related to using the "
                    "grasshopper script"
    )

    @model_validator(mode='after')
    def validate_parameter_names(self):
        """
        Validate that the parameter names in the connections are valid
        """
        errors: List[InitErrorDetails] = []

        for connection in self.Connections:
            component_name_to = self.get_connection_component_name(
                    connection.To, errors
                )
            component_name_from = self.get_connection_component_name(
                    connection.From, errors
                )

            # map to list of valid components
            if component_name_to is None:
                continue
            valid_component_to = find_valid_component_by_name(
                valid_components,
                component_name_to,
                errors
            )
            if component_name_from is None:
                continue
            valid_component_from = find_valid_component_by_name(
                valid_components,
                component_name_from,
                errors
            )

            # extract parameter from valid component data
            find_valid_parameter_by_name(
                valid_component=valid_component_to,
                parameter_name=connection.To.ParameterName,
                input_output_type='input',
                errors=errors
            )
            find_valid_parameter_by_name(
                valid_component=valid_component_from,
                parameter_name=connection.From.ParameterName,
                input_output_type='output',
                errors=errors
            )

        #     input_parameter_type = valid_parameter_to.DataType
        #     output_parameter_type = valid_parameter_from.DataType

        #     if input_parameter_type != output_parameter_type:
        #         raise ValueError(
        #             f"Parameter types do not match for the connection between "
        #             f"{component_name_from} and {component_name_to}. The input"
        #             f"parameter {connection.To.ParameterName} of "
        #             f"{component_name_to} expects a {input_parameter_type} "
        #             f"type, but the output parameter "
        #             f"{connection.From.ParameterName} of {component_name_from}"
        #             f"of {component_name_from} is of type"
        #             f"{output_parameter_type}. Please make sure the types "
        #             f"match.")
        if len(errors) > 0:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=errors,
            )
        return self

    def get_connection_component_name(
        self,
        connection_detail: Union[InputConnectionDetail,
                                 OutputConnectionDetail],
        errors: List[InitErrorDetails]
    ):
        id = connection_detail.Id

        script_component = next(
            (comp for comp in self.Components if comp.Id == id),
            None
        )
        if script_component is None:
            errors.append(InitErrorDetails(
                type=PydanticCustomError(
                    "",
                    f"Component with id {id} not found")
            ))

        return script_component.Name


class Example(BaseModel):
    Description: str
    GrasshopperScriptModel: GrasshopperScriptModel


def find_valid_component_by_name(
    valid_components: ValidComponents,
    name: str,
    errors: List[InitErrorDetails]
):
    """
    Find the valid component with the given name from the list of valid
    components.
    Raises a ValueError if the component is not found.
    """
    valid_component = next(
        (comp for comp in valid_components.Components if comp.Name == name),
        None
    )
    if valid_component is None:
        # this should not happen as the component name is validated
        # before this validation
        errors.append(InitErrorDetails(
            type=PydanticCustomError(
                "",
                f"Component with name {name} not found")
        ))
    return valid_component


def find_valid_parameter_by_name(
    valid_component: ValidComponent,
    parameter_name: str,
    input_output_type: Literal["input", "output"],
    errors: List[InitErrorDetails]
):
    """
    Find the valid input/output with the given parameter name from the list of
    valid inputs/outputs of a component.
    Raises a ValueError if the input/output is not found.
    """
    if input_output_type == "input":
        valid_input_outputs = [inputs.Name for
                               inputs in valid_component.Inputs]
    else:
        valid_input_outputs = [outputs.Name for
                               outputs in valid_component.Outputs]
    valid_parameter = next(
        (input_output for input_output in valid_input_outputs
            if input_output == parameter_name),
        None
    )
    if valid_parameter is None:
        errors.append(InitErrorDetails(
            type=PydanticCustomError(
                "",
                f"Component '{valid_component.Name}' does not have an "
                f"{input_output_type} parameter called "
                f"'{parameter_name}'. Please choose a valid parameter "
                f"from this list: {valid_input_outputs}."
            )
        ))
    return valid_parameter


class StrategyRating(BaseModel):
    input_adherence: str = Field(
        ..., description=textwrap.dedent(
            """
            in words, and with reference to 'inputs' in the 'Problem Description'
            critically evaluate if all inputs have been included in the plan.
            e.g. as slider, point, or panel components
            """
        )
    )
    detail: List[str] = Field(
        ..., description=textwrap.dedent(
            """
            for each strategy step, in words, critically evaluate whether the
            single component can truthefully implement everything in the steps
            description.
            """
        )
    )
    validation_errors: str = Field(
        ..., description=textwrap.dedent(
            """
            In words critically consider very carefully any component
            validation errors and whether any substitutions would
            faithfully represent the original strategy.
            Explain each one in turn.
            """
        )
    )
    susbstitution_recommendations: Optional[List[str]] = Field(
        ..., description=textwrap.dedent(
            """
            For each validation error give one single recommended substitution
            for the missing component
            """
        )
    )
    other_advice: Optional[str] = Field(
        ..., description=textwrap.dedent(
            """
            any other advice to address any issues mentioned in
            reasoning
            """
        )
    )
    score: int = Field(..., description=textwrap.dedent(
            """
            The score considering all of the above from 0 to 10.
            """
        )
    )


class ProblemStatement(BaseModel):
    inputs: List[str] = Field(
        ..., description=textwrap.dedent(
            """
            list of all inputs required for the script to function
            e.g. Number Slider, Panel, Point components.
            Include their assumed value if appropriate
            """)
    )
    outputs: List[str] = Field(
        ...,
        description="expected outputs of the script based on the description"
    )
    assumptions: Optional[List[str]] = Field(
        ...,
        description="any assumptions that you need to make before getting"
        "started"
    )
