from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional, Union
from data.components import load_components

components_dict = load_components()


class NumberSlider(BaseModel):
    Name: Literal["Number Slider"]
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )
    Value: Optional[str] = Field(
        None,
        alias='Value',
        description="The range of values for the Number Slider. "
                    "In the format '<start>..<default>..<end>'. "
                    "Give a decent range of values to allow for flexibility"
    )


class Panel(BaseModel):
    Name: Literal["Panel"]
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )
    Value: Optional[str] = Field(
        None,
        alias='Value',
        description="The text for the Panel Component. "
                    "In the format '<text>'"
    )


class Point(BaseModel):
    Name: Literal["Panel"]
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )
    Value: Optional[str] = Field(
        None,
        alias='Value',
        description="The 3D coordinates for the Point Component. "
                    "In the format '<x>,<y>,<z>'"
    )


class Component(BaseModel):
    Name: str = Field(
        ...,
        description="The name of the component to be added. Only standard "
                    "grasshopper components are allowed"
    )
    Id: int = Field(
        ...,
        description="A unique identifier for the component, starting from 1 "
                    "and counting upwards"
    )


    @field_validator("Name")
    @classmethod
    def validate_name_exists(cls, v):
        name_iterator = (component["Name"] for component in components_dict)
        if v not in name_iterator:
            raise ValueError(f"The component {v} could not be found, either "
                             "there is a typo or it does not exist. Please "
                             "choose a valid component.")
        return v


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


class GrasshopperScriptModel(BaseModel):
    """
    A representation of a grasshopper script with all grasshopper components
    and the connections between them.
    Use Number Slider for variable inputs to the script
    """
    ChainOfThought: str = Field(
        ...,
        description="step by step rational explaining how the script acheives "
                    "the aim, including the main components used"
    )
    Additions: List[Union[Component, NumberSlider, Panel, Point]] = Field(
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
