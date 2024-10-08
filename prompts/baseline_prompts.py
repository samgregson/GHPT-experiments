system_prompt = """
You are a Grasshopper Expert and are going to help create Grasshopper Definitions.
Keep the answers short and concise.
Make sure you create and connect a component for every non-optional input
If you're not sure about the answer, but think there's additional information that could help you, please ask for that information.

Always use the given format, avoid any devitation.
"""

prompt_template = r"""
// Question : How do I add two numbers inside of Grasshopper?
// Reasoning: To add two numbers we need to Add. There is an Addition component that performs this function. We need to create two numbers the user can edit, we can use the Number Slider for both numbers. And then we can Connections all of the components together
// JSON:
{
	"Advice": "Make sure to set the number sliders to the correct value",
	"Additions": [
		{
			"Name": "Number Slider",
			"Id": 1,
			"value": "0..25..100"
		},
		{
			"Name": "Number Slider",
			"Id": 2,
			"value": "-50..25..100"
		},
		{
			"Name": "Addition",
			"Id": 3
		}
	],
	"Connections": [
		{
			"To": {
				"Id": 3,
				"ParameterName": "A"
			},
			"From": {
				"Id": 1,
				"ParameterName": "number"
			}
		},
		{
			"To": {
				"Id": 3,
				"ParameterName": "B"
			},
			"From": {
				"Id": 2,
				"ParameterName": "number"
			}
		}
	]
}

// Question: How do I create a cup shape in grasshopper
// Reasoning: To create a cup shape in Grasshopper, we"ll first create a circle using a "Circle CNR" component, which will act as the base of the cup. Then, we will use a "Move" component to move the base circle vertically to create the upper rim of the cup. To create the body of the cup, we"ll loft these two circles using a "Loft" component.
// JSON:
{
	"Advice": "Remember, to properly define the cup\"s dimensions using the number slider",
	"Additions": [
		{
			"Name": "Circle CNR",
			"Id": 1
		},
		{
			"Name": "Move",
			"Id": 2
		},
		{
			"Name": "Loft",
			"Id": 3
		}
	],
	"Connections": [
		{
			"To": {
				"Id": 2,
				"ParameterName": "Geometry"
			},
			"From": {
				"Id": 1,
				"ParameterName": "Circle"
			}
		},
		{
			"To": {
				"Id": 3,
				"ParameterName": "Curves"
			},
			"From": {
				"Id": 1,
				"ParameterName": "Circle"
			}
		},
		{
			"To": {
				"Id": 3,
				"ParameterName": "Curves"
			},
			"From": {
				"Id": 2,
				"ParameterName": "Geometry"
			}
		}
	]
}

// Question: How do I create a twisty skyscraper?
// Reasoning: We can create the "twist" using the twist component, so lets extrude a rectangle and twist it!
// JSON:
{
	"Advice": "Make sure to use reasonable inputs or the skyscraper will look weird",
	"Additions": [
		{
			"Name": "Rectangle",
			"Id": 1
		},
		{
			"Name": "Number Slider",
			"Id": 2,
			"Value": "0..50..100"
		},
		{
			"Name": "Unit Z",
			"Id": 3
		},
		{
			"Name": "Extrusion",
			"Id": 4
		},
		{
			"Name": "Number Slider",
			"Id": 5,
			"Value": "0..90..360"
		},
		{
			"Name": "Line",
			"Id": 6
		},
		{
			"Name": "Point",
			"Id": 7,
			"value": "{0,0,0}"
		},
		{
			"Name": "Point",
			"Id": 8,
			"value": "{0,0,250}"
		},
		{
			"Name": "Twist",
			"Id": 9
		},
		{
			"Name": "Solid Union",
			"Id": 10
		},
		{
			"Name": "Brep Join",
			"Id": 11
		}
	],
	"Connections": [
		{
			"To": {
				"Id": 4,
				"ParameterName": "Base"
			},
			"From": {
				"Id": 1,
				"ParameterName": "Rectangle"
			}
		},
		{
			"To": {
				"Id": 3,
				"ParameterName": "Factor"
			},
			"From": {
				"Id": 2,
				"ParameterName": "Number"
			}
		},
		{
			"To": {
				"Id": 9,
				"ParameterName": "Angle"
			},
			"From": {
				"Id": 5,
				"ParameterName": "Number"
			}
		},
		{
			"To": {
				"Id": 4,
				"ParameterName": "Direction"
			},
			"From": {
				"Id": 3,
				"ParameterName": "Unit vector"
			}
		},
		{
			"To": {
				"Id": 9,
				"ParameterName": "Geometry"
			},
			"From": {
				"Id": 4,
				"ParameterName": "Extrusion"
			}
		},
		{
			"To": {
				"Id": 6,
				"ParameterName": "Start Point"
			},
			"From": {
				"Id": 7,
				"ParameterName": "Point"
			}
		},
		{
			"To": {
				"Id": 6,
				"ParameterName": "End Point"
			},
			"From": {
				"Id": 8,
				"ParameterName": "Point"
			}
		},
		{
			"To": {
				"Id": 10,
				"ParameterName": "Breps"
			},
			"From": {
				"Id": 9,
				"ParameterName": "Geometry"
			}
		},
		{
			"To": {
				"Id": 11,
				"ParameterName": "Breps"
			},
			"From": {
				"Id": 10,
				"ParameterName": "Result"
			}
		},
		{
            "To": {
                "Id": 9,
                "ParameterName": "Axis"
                },
            "From": {
                "Id": 6,
                "ParameterName": "Line"
            }
		}
	]
}

// Question: {QUESTION}
// Reasoning:
""".replace("{", "{{").replace("}", "}}").replace("{{QUESTION}}", "{QUESTION}")
