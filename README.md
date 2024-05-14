[![Lint and Test](https://github.com/samgregson/GHPT-experiments/actions/workflows/python-app.yml/badge.svg)](https://github.com/samgregson/GHPT-experiments/actions/workflows/python-app.yml)

# GHPT-experiments

This is inspired by GHPT: https://github.com/enmerk4r/GHPT

The aim is to "flow engineer" a Large Language Model (LLM) powered program to generate Grasshopper3d scripts based on a user prompt as input.

This repo goes as far as generating JSON formatted string which can be ingested by a custom Grasshopper component. The JSON string structure is aligned with the structure in the original GHPT repo (see above).

A modified GHPT version (saved in a separate branch) can be found here:

https://github.com/samgregson/GHPT/tree/llm-result-as-input

This allows JSON input to be used directly to allow for testing the output of the colab notebook to aid development and test validity of generated JSON.

![image](https://github.com/samgregson/GHPT-colab-experiments/assets/12054742/5c7465b6-30aa-430e-b14e-5cb4a56c3988)

## Get Started (in VS Code)
* clone repo
* run `pip install -r requirements.txt` to install dependancies
* run `pip install jupyter` to install dependancies
* run `pip install -e .` to install the project module
* set up `OPENAI_API_KEY` in `.env` file (assuming you have set one up)

## Built With

* [Instructor](https://jxnl.github.io/instructor/)
* [OpenAI](https://platform.openai.com/)

## Contributing

There are two ways to contribute to the notebook files, via Google Colab or locally in and IDE such as VS Code

1. clone the repository
2. create a new branch with suitable name to reflect the changes you will make

### Colab

3. open the colab notebook in google colab
4. modify the notebook as required
5. "save a copy in github"

![image](https://github.com/samgregson/GHPT-colab-experiments/assets/12054742/c5816c64-827f-4c4c-ac01-9774ba85d896)
6. select the correct branch and write a suitable commit message (not as below)

![image](https://github.com/samgregson/GHPT-colab-experiments/assets/12054742/2308000f-e4c3-452b-8251-2846948a248b)

7. make a pull request

### Local

3. modify any file
4. push changes to your new branch
5. make a pull request

## Acknowledgements

* This is inspired by GHPT: https://github.com/enmerk4r/GHPT

