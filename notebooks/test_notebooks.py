import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest

@pytest.mark.parametrize("notebook", ['notebooks/ghpt_baseline.ipynb','notebooks/ghpt_instructor.ipynb'])
def test_notebooks(notebook):
    """
    Test function to execute and validate a Jupyter notebook.

    Args:
        notebook (str): The path to the Jupyter notebook file.

    Raises:
        AssertionError: If the notebook is empty or execution fails.
    """
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        try:
            assert ep.preprocess(nb) is not None, f"Got empty notebook for {notebook}"
        except Exception:
            assert False, f"Failed executing {notebook}"