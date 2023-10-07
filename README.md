# Analogical Reasoning 

This README explains how to utilize our Python script. The provided script is programmed to perform various tasks related to analogy, using OpenAI's GPT-4. These tasks include sentence or story analogy extraction and story generation. Follow the instructions given below to use the provided script.

## Table of Contents
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Command Line Arguments](#command-line-arguments)
- [Supported Tasks](#supported-tasks)
- [License](#license)

## Prerequisites
Ensure that the following requirements are met before running the code:

- Python 3.6 or higher
- Access to OpenAI's GPT-4, which requires an API key.

## How to Use
1. Clone this repository to your local system.
2. Install the necessary Python packages with the following command:
    ```bash
    pip install -r requirements.txt
    ```
3. Export your API key for GPT- as an environmental variable:
    ```bash
    export API_KEY="..." 
    ```
4. Run the script. The basic command usage is as follows:
    ```bash
    python main.py -t [task] -k [times for story analogy generation]
    ```
    Replace [task] with the task type and [-k] with the number of times you want to run the story analogy generation task.

   To see different possible commands, use `--help`. 
   
## Command Line Arguments
The script accepts these command-line arguments:

- `-t` or `--task`: Specifies the task to run. It's required and can be either 'sentence', 'story_generate', 'story_analogy', 'name_generate' or 'name_analogy'.
- `-k` or `--k`: Specifies the number of times you would like to generate story analogies. It's optional, with a default value of 1.

## License
This project is available under the MIT License. You can freely modify and use it as per your needs. Please keep in mind OpenAI's terms and policies if you use GPT-4.