import pytest
from pipeline.pipeline import pipe_get_examples


def test_example_nearest_fail():

    input = "create a cup"

    examples = pipe_get_examples(input)

    with pytest.raises(ValueError) as e:
        input == examples[0]
    assert "sorting incorrect" in str(e.value)

    

def test_example_embedding_None_fail():

    input = "create a cup"

    examples = pipe_get_examples(input)

    with pytest.raises(ValueError) as e:
        examples[0].Embedding is not None
    assert "Embedding has a value" in str(e.value)