import os
import csv
import argparse
import torch
from datasets import load_dataset

# Define command line argument parsing
parser = argparse.ArgumentParser(description='Batch process evaluation of models with different datasets.')
parser.add_argument('--sentence_length', '-s', type=str, required=True,
                    help='Task to be performed: S1, S10, or S30.')
parser.add_argument('--model_name', '-mn', type=str, required=True,
                    help='Model name, corresponds to the folder name containing the model files.')
parser.add_argument('--model_hug', '-mh', type=str, required=True,
                    help='Hugging Face identifier for the model (e.g., meta-llama/Llama-2-7b-chat-hf).')
parser.add_argument('--model_loc', '-ml', type=str, required=True,
                    help='The location of modle')
parser.add_argument('--batch_size', '-b', type=int, default=8,
                    help='Number of inputs to process in each batch. Adjust based on memory availability.')

args = parser.parse_args()

# Set up environment and cache directory
cache_dir = f"{args.model_loc}"
os.environ["TRANSFORMERS_CACHE"] = cache_dir

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(args.model_hug, cache_dir=cache_dir)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(args.model_hug, torch_dtype=torch.bfloat16, cache_dir=cache_dir, device_map="auto")

# Set up pipeline
text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, return_full_text=False)

def batch_process(rows, task_name, model_name):
    prompts = []
    for row in rows:
        sentence = row['Sentence']
        story = row.get('Story', '')  # For tasks other than S1, this gets the story.
        options = row['Options']

        prompt = f"""
Which of the following is the most analogous story to the target story?

Note: Only generate the index without any additional text. 

Target Story:
{story if task_name != "S1" else sentence}

Options:
{options}

Answer:
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
        if model_name.startswith("llama"):
            prompt = f"""
<<SYS>>
You're are a helpful Assistant, and you only response to the "Assistant"
Remember, maintain a natural tone. Be precise, concise, and casual. Keep it short\n
<</SYS>>
[INST]
User:{prompt}
[/INST]\n
Assistant:
"""
        prompts.append(prompt)

    # Generate responses for the batch of prompts
    responses = text_gen_pipeline(prompts, do_sample=True, temperature=0.3, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id, max_length=3500)
    # Update rows with results
    for row, response in zip(rows, responses):
        row['Result'] = response[0]['generated_text']

    return rows

def main():
    task_name = args.sentence_length
    batch_size = args.batch_size
    model_name = args.model_name
    output_file = f'result/T1{task_name}-{args.model_name}.csv'
    
    # Define fields for CSV based on the task
    fields = ["Index", "Sentence", "Story", "Options", "Label", "Result"] if task_name != "S1" else ["Index", "Sentence", "Options", "Label", "Result"]
    dataset = load_dataset("jhu-clsp/AnaloBench", f"T1{task_name}-Subset")
    with open(output_file, 'w', newline='') as outfile:
        reader = dataset["train"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()

        batch = []
        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                processed_batch = batch_process(batch, task_name, model_name)
                writer.writerows(processed_batch)
                batch = []

        # Process the remaining batch
        if batch:
            processed_batch = batch_process(batch, task_name, model_name)
            writer.writerows(processed_batch)

if __name__ == "__main__":
    main()