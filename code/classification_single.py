import pandas as pd
import random
import csv
import re
import torch
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer

# To use llama models with HuggingFace, you'll have to uncomment the two lines shown below and replace "YOUR_TOKEN" with your actual HuggingFace token:
# from huggingface_hub import login
# login(token="YOUR_TOKEN")


# Function to generate completion for a series of prompts and return the results
def batch_generate_completions(prompts, model, tokenizer, temperature=0.3, top_p=0.95, max_tokens=300):
    input_ids = tokenizer(prompts, return_tensors='pt', padding=True, truncation=True).input_ids.to(device)
    samples = model.generate(input_ids, temperature=temperature, top_p=top_p, do_sample=True, max_length=max_tokens + input_ids.shape[1])
    
    generated_sequences = []
    for i in range(len(prompts)):
        generated_sequence = samples[i][input_ids.shape[1]:]

        sequence_text = tokenizer.decode(generated_sequence, skip_special_tokens=True)
        generated_sequences.append(sequence_text.strip())
    del input_ids
    del samples
    return generated_sequences

# Function to process a batch and write it to the CSV file
def write_batch_to_csv(batch_info, batch_results, csvwriter, task_name):
    for info, result in zip(batch_info, batch_results):
        if task_name != "S1":
            index, sentence, story, options, label = info
            csvwriter.writerow({'Index': index, 'Sentence': sentence, 'Story': story, 'Options': options, 'Label': label, 'Result': result})
        else:
            index, sentence, options, label = info
            csvwriter.writerow({'Index': index, 'Sentence': sentence, 'Options': options, 'Label': label, 'Result': result})


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Evalute models with different datasets')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `S1`: Evaluate models using an existing dataset consisting of single-sentence entries.'
                             '\n (2) `S10`: Evaluate models using an existing dataset containing sets of 10 sentences.'
                             '\n (3) `S30`: Evaluate models using an existing dataset with 30-sentence groups.',
                        required=True)
    parser.add_argument('--model_name', '-mn', type=str, default=None,
                        help='It specifies the model name, which should also be the name of the folder containing the model files.'
                             '\n Note that this script only supports models that are designed to run on a single GPU.',
                        required=True)
    parser.add_argument('--model_hug', '-mh', type=str, default=None,
                        help='Huggingface identifier for the model. For example meta-llama/Llama-2-7b-chat-hf',
                        required=True)
    parser.add_argument('--batch_size', '-b', type=int, default=None, required=True)
    args = parser.parse_args()
    task_name = args.task
    model_name = args.model_name
    model_hug = args.model_hug
    # Example for model_name and model_hug: 
    # model_name = "xwinlm13"
    # model_hug = "Xwin-LM/Xwin-LM-13B-V0.1"
    batch_size = args.batch_size

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print(f"Using device: {device}")

    torch.cuda.empty_cache()
    
        
    # Load the model and tokenizer
    cache_dir = f"/data/danielk/xye23/{model_name}"
    tokenizer = AutoTokenizer.from_pretrained(model_hug, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(model_hug, 
                                                 torch_dtype=torch.bfloat16, 
                                                 cache_dir=cache_dir, 
                                                 attn_implementation="flash_attention_2").to(device)
    tokenizer.pad_token = tokenizer.eos_token

    # Set batch size
    if task_name != "S1":
        fields = ["Index", "Sentence", "Story", "Options", "Label", "Result"]
    else:
        fields = ["Index", "Sentence", "Options", "Label", "Result"]

    with open(f'data/{task_name}-{model_name}.csv', 'w') as f:
        csvwriter = csv.DictWriter(f, fieldnames=fields)
        csvwriter.writeheader()

    # Read the file and process in batches
    print(f"Writing: {model_name}")
    with open(f'data/{task_name}.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        batch_prompts = []
        batch_info = []
        
        for row in reader:
            index = row['Index']
            sentence = row['Sentence']
            if task_name != "S1":
                story = row['Story']
            options = row['Options']
            label = row['Label']
            prompt = f"""
    Which of the following is the most analogous sentence to the target sentence?

    Note: Only generate a letter from [A, B, C, D] without any additional text. 

    Target Sentence:
    {story if task_name != "S1" else sentence}

    Options:
    {options}
    """
            if model_name.startswith("xwin") or model_name.startswith("wizard"):
                prompt = f"""
    A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. 
    USER: {prompt}
    ASSISTANT: 
    """
            if model_name.startswith("zephyr") or model_name.startswith("tulu"):
                prompt = f"""
    <|user|>
    {prompt}
    <|assistant|>

    """
            
            if model_name.startswith("ultra"):
                prompt = f"""
    USER: {prompt}
    ASSISTANT: 
    """
            batch_prompts.append(prompt)
            if task_name != "S1":
                batch_info.append((index, sentence, story, options, label))
            else:
                batch_info.append((index, sentence, options, label))  
            
            if len(batch_prompts) == batch_size:
                results = batch_generate_completions(batch_prompts, model, tokenizer)
                with open(f'data/{task_name}-{model_name}.csv', 'a') as f:
                    csvwriter = csv.DictWriter(f, fieldnames=fields)
                    write_batch_to_csv(batch_info, results, csvwriter, task_name)
                batch_prompts = []
                batch_info = []
        
        # Process the final batch if it's not empty
        if batch_prompts:
            results = batch_generate_completions(batch_prompts, model, tokenizer)
            with open(f'data/{task_name}-{model_name}.csv', 'a') as f:
                csvwriter = csv.DictWriter(f, fieldnames=fields)
                write_batch_to_csv(batch_info, results, csvwriter, task_name)
