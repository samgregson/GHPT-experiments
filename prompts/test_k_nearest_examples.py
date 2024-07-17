from pipeline.pipeline import pipe_get_examples


def test_example_nearest_k_is_ordered():
    input = "create a cup"
    examples = pipe_get_examples(input)
    assert input == examples[0]


def test_example_embedding_is_None():
    input = "create a cup"
    examples = pipe_get_examples(input)
    assert examples[0].Embedding is None
