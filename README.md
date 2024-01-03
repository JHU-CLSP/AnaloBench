# Analogical Reasoning 

This README explains how to utilize our Python script. The provided script is programmed to perform various tasks related to analogy, using OpenAI's GPT-4. These tasks include sentence or story analogy classification. Follow the instructions given below to use the provided script.

## Overview

The scripts available in this repository are designed to accomplish different objectives, from dataset generation to model evaluation. These scripts are organized to work together, implementing an end-to-end pipeline.

The tasks are categorized into single-sentence (`S1`) and grouped-sentence tasks (`S10` and `S30`), depending on the number of sentences involved in the classification.

## Repository Structure

- `classification_multi.py`: Evaluates models on multi-sentence classification tasks across distributed GPUs.
- `classification_single.py`: Similar to `classification_multi.py`, but for single-GPU setups.
- `data_generation.py`: Generates datasets for various classification tasks.
- `evaluation.py`: Analyzes the performance of models by comparing generated results against ground truth labels.

## Quick Start

### Requirements

- Python 3.x
- PyTorch
- Transformers library from Hugging Face
- Pandas

Additionally, access to Hugging Face models (like llama) might require a Hugging Face account and a personal access token.

### Usage

#### Dataset Generation

Generate the base dataset for classification:

```bash
python data_generation.py --task generate_base_classification
```

Generate a dataset tailored for single sentence classification tasks:

```bash
python data_generation.py --task generate_s1_classification
```

Generate a dataset for 10-sentence classification tasks:

```bash
python data_generation.py --task generate_s10_classification
```

Generate a dataset for 30-sentence classification tasks:

```bash
python data_generation.py --task generate_s30_classification
```

#### Model Evaluation

To evaluate a model with a specific dataset and configuration, use one of the following scripts:

For multi-GPU setups:

```bash
python classification_multi.py --task <TASK_NAME> --model_name <MODEL_NAME> --model_hug <HUGGINGFACE_MODEL> --batch_size <BATCH_SIZE>
```

For single-GPU setups:

```bash
python classification_single.py --task <TASK_NAME> --model_name <MODEL_NAME> --model_hug <HUGGINGFACE_MODEL> --batch_size <BATCH_SIZE>
```

Replace `<TASK_NAME>`, `<MODEL_NAME>`, `<HUGGINGFACE_MODEL>`, and `<BATCH_SIZE>` with your desired value.

#### Evaluation of Results

Run the evaluation script to output accuracy and other relevant metrics:

```bash
python evaluation.py
```

### Customization

To use a specific Hugging Face model, you may need to log in with your Hugging Face token:

```python
from huggingface_hub import login
login(token="YOUR_TOKEN")
```

You can uncomment these lines in `classification_multi.py` or `classification_single.py` and replace `"YOUR_TOKEN"` with your actual Hugging Face token.

### Important Notes

- The scripts are set up to read and write data from a `data` directory. Ensure this directory exists and has the correct structure and contents as per your dataset requirements.
- The models are loaded from a specified cache directory in the `classification_*.py` scripts. You may need to update the `cache_dir` variable to match your local setup.

## Support

If you encounter any issues or have questions regarding the scripts, please submit an issue in this repository.

## License
This project is available under the MIT License. You can freely modify and use it as per your needs. Please keep in mind OpenAI's terms and policies if you use GPT-4.