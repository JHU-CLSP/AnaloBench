# Analogical Reasoning

This README provides an overview and usage instructions for the provided Python script, which employs the OpenAI's GPT-4 in executing analogy tasks. This code allows you to undertake analogy comparisons between sentences or stories and renders predictions based on these tasks. Follow the instructions detailed below to successfully utilize this code.

## Table of Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [Command Line Arguments](#command-line-arguments)
- [Tasks Supported](#tasks-supported)
- [License](#license)

## Requirements
Before the deployment of this code, ensure that you meet the following prerequisites:

- Python 3.6 or higher
- An API key for GPT-4 (attainable from OpenAI)

## Usage
1. Clone this repository to your local machine.
2. Install the required Python packages by executing the command:
    ```bash
    pip install -r requirements.txt
    ```
3. Modify the config.py file to contain your GPT-4 API key. Replace 'YOUR_API_KEY' with your actual API key:
    ```python
    GPT4KEY = { "API_KEY": "YOUR_API_KEY" }
    ```
4. Run the script with the appropriate task and required inputs. Below is the basic usage:
    ```bash
    python code/main.py -t [task] -s1 [input1] -s2 [input2]
    ```
    Replace [task] with a supported task type, [input1] with your first input (sentence or story), and [input2] with your second input (sentence or story).

## Command Line Arguments
 The script accepts the following command-line arguments:

 - `-t` (or `--task`): Specifies the task you intend to execute. This argument is mandatory and must be either of the following:
   * `sentence`: Executes a sentence analogy task.
   * `story_generate`: Executes a story generation task.
   * `story_analogy`: Executes a story analogy task.
   * `name`: Currently unsupported; reserved for future use.
 - `-s1` (or `--sent1`): The initial input, which can be a sentence or a story. This argument is mandatory.
 - `-s2` (or `--sent2`): The subsequent input, which can also be a sentence or a story. This argument is also mandatory.

## Tasks Supported
The script currently supports the following tasks:

- `sentence` : If you select the "sentence" task, the program examines two input sentences and identifies the analogies and incorrect analogies between them.
- `story_generate` : If you opt for the "story_generate" task, the script generates diverse stories using the two provided input sentences or stories.
- `story_analogy` : For the "story_analogy" task, the code identifies the analogies and incorrect analogies between two stories.
- `name` : The "name" task is currently under construction and has no functionality at the moment.

## License
This code is available under the MIT License. Feel free to modify and put it to use, as per your requirements. If you make use of GPT-4, ensure your compliance with OpenAI's terms and policies.