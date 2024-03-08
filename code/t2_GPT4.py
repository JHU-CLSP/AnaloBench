import requests
import json
import argparse
import csv
from data_generation import load_and_map_clustered_sentences

# To use GPT4, you'll have to uncomment the following line shown below and replace "YOUR_KEY" with your actual OpenAI key:
# API_KEY = "YOUR_KEY"

def generate_chat_completion(messages, temperature: float, top_p: float, model="gpt-4-1106-preview",
                             max_tokens: int = 1000):
    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrival Task Evaluation. Use --help to see the options.')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `R1`: Evaluate models using an existing dataset consisting of single-sentence entries.'
                             '\n (2) `R10`: Evaluate models using an existing dataset containing sets of 10 sentences.'
                             '\n (3) `R30`: Evaluate models using an existing dataset with 30-sentence groups.',
                        required=True)
    args = parser.parse_args()
    command_task = args.task

    if command_task == "R1":
        task = 0
    elif command_task == "R10":
        task = 10
    else:
        task = 30

    sentence_bank, clusters, story_clusters = load_and_map_clustered_sentences(task)

    if task != 0:
        fields = ["Index", "Sentence", "Story", "Options", "Indices", "Result"]
    else:
        fields = ["Index", "Sentence", "Options", "Indices", "Result"]
    with open(f'data/T2S{task if task != 0 else 1}-GPT4.csv', 'w') as f:
        csvwriter = csv.DictWriter(f, fieldnames=fields)
        csvwriter.writeheader()
    with open('data/AnaloBench-T2-Base.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            index = row['Index']
            sentence = row['Sentence']
            if task != 0:
                story = story_clusters[sentence]
            options = [int(i) for i in row['Options'].split(",")]
            indices = [int(i) for i in row['Indices'].split(",")]
            if task != 0:
                options = [f"{i+1}. {story_clusters[sentence_bank[int(option)]]}" for i, option in enumerate(options)]
            else:
                options = [f"{i+1}. {sentence_bank[int(option)]}" for i, option in enumerate(options)]
            options = "\n".join(options)
            prompt = f"""
    Retrieve the top 10 analogous stories from the sentence bank for the following target story:
    NOTE: Only generate an index number without any additional text. For example: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    Target Story:
    {story if task != 0 else sentence}

    Sentence Bank:
    {options}

    """
            prompt = [
                {"role": "user", "content": prompt}
            ]
            result = generate_chat_completion(prompt, temperature=0.3, top_p=0.95, max_tokens=4000)
            with open(f'data/T2S{task if task != 0 else 1}-GPT4.csv', 'a') as f:
                csvwriter = csv.DictWriter(f, fieldnames=fields)
                if task != 0:
                    csvwriter.writerow({'Index': index, 'Sentence': sentence, "Story": story, "Options": row['Options'], "Indices": row['Indices'], "Result": result})
                else:
                    csvwriter.writerow({'Index': index, 'Sentence': sentence, "Options": row['Options'], "Indices": row['Indices'], "Result": result})