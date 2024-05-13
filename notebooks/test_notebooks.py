import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest

# file path needed to work with pytest
dir_path = os.path.dirname(os.path.realpath(__file__))
notebooks = [os.path.join(dir_path, 'ghpt_baseline.ipynb'), os.path.join(dir_path, 'ghpt_instructor.ipynb')]

@pytest.mark.parametrize("notebook", notebooks)
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
        except Exception as e:
            assert False, f"Failed executing {notebook}: {str(e)}"