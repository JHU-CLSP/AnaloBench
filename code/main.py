import csv
import config
import prompts
import argparse
from tqdm import tqdm
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="analogy tasks")
    parser.add_argument('-t', '--task', type=str, help='The task that you want to do. Possible options are `sentence` and `story_generate` and `story_analogy` ', required=True)
    parser.add_argument('-k', '--k', type=int, help='The number of times we prompt the model for generating analogies.', required=False, default=1)
    args=parser.parse_args()
    return args

if __name__ == '__main__': 
    args = parse_args()
    task = args.task
    key = config.GPT4KEY["API_KEY"]
    sent_data = pd.read_csv("sentences.csv")
    num_generation = args.k
    if task == "sentence":
        fields = ["Index", "Sentence1", "Sentence2", "Correct_Analogy"]
        filename = "sent_analogy.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in tqdm(enumerate(sent_data.values)):
                try:
                    correct_out = prompts.generate_analogies(sent1, sent2)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise
                
                csvwriter.writerow({
                    "Index": i,
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Correct_Analogy": correct_out
                })

    elif task == "story_generate":
        fields =  ["Index", "Sentence1", "Sentence2", "Story1", "Story2"]
        filename = "story_generation.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in enumerate(sent_data.values):
                try:
                    output1 = prompts.generate_diverse_story(sent1)
                    story1 = output1["generation"]
                    style1 = output1["style"]

                    output2 = prompts.generate_diverse_story(sent2)
                    story2 = output1["generation"]
                    style2 = output1["style"]
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise

                csvwriter.writerow({
                    "Index": i,
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Story1": story1,
                    "Story2": story2,
                    "Style1": style1,
                    "Style2": style2
                })
    elif task == "story_analogy":
        for k in range(num_generation):
            fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Analogy"]
            filename_input = "story_generation.csv"
            filename_output = f"story_analogy_{k+1}.csv"

            with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
                csvreader = csv.DictReader(csvfile_input)
                csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
                csvwriter.writeheader()

                for row in tqdm(csvreader):
                    try:
                        sent1, sent2 = row["Sentence1"], row["Sentence2"]
                        story1, story2 = row["Story1"], row["Story2"]
                        correct_out = prompts.generate_analogies(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise

                    csvwriter.writerow({
                        "Index": row["Index"],
                        "Sentence1": sent1,
                        "Sentence2": sent2,
                        "Story1": story1,
                        "Story2": story2,            
                        "Analogy": correct_out
                    })
    elif task == "name":
        #TODO: currently no high quality incorrect
        pass
