inputs = [
    "Create a cylinder with a radius of 5 and a height of 10.",
    "Generate a spiral with 10 turns and a radius of 2.",
    "Create a rectangular grid of 5 by 5 points with a spacing of 10 in the x and y directions.",
    "Generate a sphere with a radius of 10 at the origin.",
    "Create a series of 10 circles with radii increasing by 1 for each subsequent circle.",
    "Generate a 3D grid of 5x5x5 spheres with a spacing of 10 in the x, y, and z directions.",
    "Create a line from the origin to the point (10,10,10).",
    "Generate a series of 10 squares with side lengths increasing by 2 for each subsequent square.",
    "Create a cone with a base radius of 5 and a height of 10.",
    "Generate a torus with a tube radius of 2 and a path radius of 5.",
    "Create a triangular grid of 5 by 5 points with a spacing of 10 in the x and y directions.",
    "Generate a series of 10 rectangles with lengths and widths increasing by 2 for each subsequent rectangle.",
    "Create a pyramid with a base side length of 5 and a height of 10.",
    "Generate a series of 10 lines with lengths increasing by 2 for each subsequent line.",
    "Create a hexagonal grid of 5 by 5 points with a spacing of 10 in the x and y directions.",
    "Generate a series of 10 hexagons with side lengths increasing by 1 for each subsequent hexagon.",
    "Create a 3D grid of 5x5x5 cubes with a spacing of 10 in the x, y, and z directions. The size of the cubes should be determined by each cube's proximity to a random point on the grid such that at distance 0 the cube has dimensions 0 and at distance 1 the cube has dimensions 1.",
    "Generate a series of 10 cylinders with radii increasing by 1 and heights increasing by 2 for each subsequent cylinder.",
    "Create a series of 10 cones with base radii increasing by 1 and heights increasing by 2 for each subsequent cone.",
    "Generate a series of 10 pyramids with base side lengths increasing by 1 and heights increasing by 2 for each subsequent pyramid.",
]

outputs = [
    #     "Create a cylinder with a radius of 5 and a height of 10.",
    """
    {
        "ChainOfThought": "To create a cylinder with a radius of 5 and a height of 10, we'll first create a Number Slider for the radius with a range of 0 to 10 and a default value of 5. Then, we'll create a Number Slider for the height with a range of 0 to 20 and a default value of 10. Finally, we'll use the Cylinder component to create a cylinder with the specified radius and height.",
        "Components": [
            {
                "Name": "Number Slider",
                "Id": 1,
                "Value": "0..5..10",
                "NickName": "Radius"
            },
            {
                "Name": "Number Slider",
                "Id": 2,
                "Value": "0..10..10",
                "NickName": "Height"
            },
            {
                "Name": "Cylinder",
                "Id": 3
            }
        ],
        "Connections": [
            {
                "From": 
                {
                    "Id": 1,
                    "ParameterName": "Value"
                },
                "To": 
                {
                    "Id": 3,
                    "ParameterName": "Radius"
                }
            },
            {
                "From": 
                {
                    "Id": 2,
                    "ParameterName": "Value"
                },
                "To": 
                {
                    "Id": 3,
                    "ParameterName": "Length"
                }
            }
        ],
        "Advice": "Make sure to set the number sliders to the correct value"
    }
    """,
    # "Generate a spiral with 10 turns and a radius of 2."
    """
    {
    "Components": [
        {
        "Id": 1,
        "Name": "Number Slider",
        "NickName": "r",
        "Value": "0..2..10"
        },
        {
        "Id": 2,
        "Name": "Number Slider",
        "NickName": "Rotations",
        "Value": "0..10..10"
        },
        {
        "Id": 3,
        "Name": "Point",
        "Value": "{0,0,0}"
        },
        {
        "Id": 4,
        "Name": "Point Polar"
        },
        {
        "Id": 5,
        "Name": "Pi"
        },
        {
        "Id": 6,
        "Name": "Multiplication"
        },
        {
        "Id": 7,
        "Name": "Number Slider",
        "NickName": "2pi",
        "Value": "0..2..10"
        },
        {
        "Id": 8,
        "Name": "Range"
        },
        {
        "Id": 9,
        "Name": "Range"
        },
        {
        "Id": 10,
        "Name": "Interpolate"
        },
        {
        "Id": 11,
        "Name": "Multiplication"
        },
        {
        "Id": 12,
        "Name": "Number Slider",
        "NickName": "",
        "Value": "0..8..10"
        }
    ],
    "Connections": [
        {
        "From": {
            "Id": 3,
            "ParameterName": "Point"
        },
        "To": {
            "Id": 4,
            "ParameterName": "Base plane"
        }
        },
        {
        "From": {
            "Id": 8,
            "ParameterName": "Range"
        },
        "To": {
            "Id": 4,
            "ParameterName": "XY angle"
        }
        },
        {
        "From": {
            "Id": 9,
            "ParameterName": "Range"
        },
        "To": {
            "Id": 4,
            "ParameterName": "Offset"
        }
        },
        {
        "From": {
            "Id": 6,
            "ParameterName": "Result"
        },
        "To": {
            "Id": 5,
            "ParameterName": "Factor"
        }
        },
        {
        "From": {
            "Id": 2,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 6,
            "ParameterName": "A"
        }
        },
        {
        "From": {
            "Id": 7,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 6,
            "ParameterName": "B"
        }
        },
        {
        "From": {
            "Id": 5,
            "ParameterName": "Output"
        },
        "To": {
            "Id": 8,
            "ParameterName": "Domain"
        }
        },
        {
        "From": {
            "Id": 11,
            "ParameterName": "Result"
        },
        "To": {
            "Id": 8,
            "ParameterName": "Steps"
        }
        },
        {
        "From": {
            "Id": 1,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 9,
            "ParameterName": "Domain"
        }
        },
        {
        "From": {
            "Id": 11,
            "ParameterName": "Result"
        },
        "To": {
            "Id": 9,
            "ParameterName": "Steps"
        }
        },
        {
        "From": {
            "Id": 4,
            "ParameterName": "Point"
        },
        "To": {
            "Id": 10,
            "ParameterName": "Vertices"
        }
        },
        {
        "From": {
            "Id": 2,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 11,
            "ParameterName": "A"
        }
        },
        {
        "From": {
            "Id": 12,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 11,
            "ParameterName": "B"
        }
        }
    ]
    }
    """,
    # "Create a rectangular grid of 5 by 5 points with a spacing of 10 in the x and y directions."
    """
    """,
    # "Generate a sphere with a radius of 10 at the origin."
    """
    {
    "Components": [
        {
        "Id": 1,
        "Name": "Sphere"
        },
        {
        "Id": 2,
        "Name": "Number Slider",
        "NickName": "",
        "Value": "0..10..10"
        },
        {
        "Id": 3,
        "Name": "Point",
        "Value": "{0,0,0}"
        }
    ],
    "Connections": [
        {
        "From": {
            "Id": 3,
            "ParameterName": "Point"
        },
        "To": {
            "Id": 1,
            "ParameterName": "Base"
        }
        },
        {
        "From": {
            "Id": 2,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 1,
            "ParameterName": "Radius"
        }
        }
    ]
    }

    """,
    # "Create a series of 10 circles with radii increasing by 1 for each subsequent circle."
    """
    {
    "Components": [
        {
        "Id": 1,
        "Name": "Series"
        },
        {
        "Id": 2,
        "Name": "Number Slider",
        "NickName": "",
        "Value": "0..10..10"
        },
        {
        "Id": 3,
        "Name": "Circle CNR"
        },
        {
        "Id": 4,
        "Name": "Point",
        "Value": "{0,0,0}"
        },
        {
        "Id": 5,
        "Name": "Number Slider",
        "NickName": "",
        "Value": "0..1..1"
        }
    ],
    "Connections": [
        {
        "From": {
            "Id": 5,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 1,
            "ParameterName": "Start"
        }
        },
        {
        "From": {
            "Id": 2,
            "ParameterName": "Value"
        },
        "To": {
            "Id": 1,
            "ParameterName": "Count"
        }
        },
        {
        "From": {
            "Id": 4,
            "ParameterName": "Point"
        },
        "To": {
            "Id": 3,
            "ParameterName": "Center"
        }
        },
        {
        "From": {
            "Id": 1,
            "ParameterName": "Series"
        },
        "To": {
            "Id": 3,
            "ParameterName": "Radius"
        }
        }
    ]
    }

    """,
    # "Generate a 3D grid of 5x5x5 spheres with a spacing of 10 in the x, y, and z directions."
    """
    """,
    # "Create a line from the origin to the point (10,10,10)."
    """
    """,
    # "Generate a series of 10 squares with side lengths increasing by 2 for each subsequent square."
    """
    """,
    # "Create a cone with a base radius of 5 and a height of 10."
    """
    """,
    # "Generate a torus with a tube radius of 2 and a path radius of 5."
    """
    """,
    # "Create a triangular grid of 5 by 5 points with a spacing of 10 in the x and y directions."
    """
    """,
    # "Generate a series of 10 rectangles with lengths and widths increasing by 2 for each subsequent rectangle."
    """
    """,
    # "Create a pyramid with a base side length of 5 and a height of 10."
    """
    """,
    # "Generate a series of 10 lines with lengths increasing by 2 for each subsequent line."
    """
    """,
    # "Create a hexagonal grid of 5 by 5 points with a spacing of 10 in the x and y directions."
    """
    """,
    # "Generate a series of 10 hexagons with side lengths increasing by 1 for each subsequent hexagon."
    """
    """,
    # "Create a 3D grid of 5x5x5 cubes with a spacing of 10 in the x, y, and z directions. The size of the cubes should be determined by each cube's proximity to a random point on the grid such that at distance 0 the cube has dimensions 0 and at distance 1 the cube has dimensions 1."
    """
    """,
    # "Generate a series of 10 cylinders with radii increasing by 1 and heights increasing by 2 for each subsequent cylinder."
    """
    """,
    # "Create a series of 10 cones with base radii increasing by 1 and heights increasing by 2 for each subsequent cone."
    """
    """,
    # "Generate a series of 10 pyramids with base side lengths increasing by 1 and heights increasing by 2 for each subsequent pyramid."
    """
    """,
]
