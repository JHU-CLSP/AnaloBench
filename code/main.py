import csv
import config
import prompts
import argparse
import pandas as pd
from tqdm import tqdm
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Spacy's English model
nlp = spacy.load('en_core_web_sm')


def similarity_check(text1, text2):
    doc1 = nlp(text1.lower())
    doc2 = nlp(text2.lower())
    
    tokens1 = " ".join([token.lemma_ for token in doc1])
    tokens2 = " ".join([token.lemma_ for token in doc2])

    # use CountVectorizer to convert text into matrix
    vectorizer = CountVectorizer().fit_transform([tokens1, tokens2])
    vectors = vectorizer.toarray()

    # calculate cosine similarity which gives us the text similarity
    csim = cosine_similarity(vectors)

    return csim[0][1]

def convert_to_list(input_str):
    # Split the input string into a list of statements
    statements = input_str.split("\n")

    result = []

    # Loop through each statement
    for statement in statements:
        paired_terms, explanation = statement.split(" | ")
        term1, term2 = paired_terms.split(" <-> ")

        # Remove leading "- " from the first term
        term1 = term1[2:] if term1.startswith('- ') else term1

        result.append((term1, term2, explanation))

    return result


def parse_args():
    parser=argparse.ArgumentParser(description="analogy tasks")
    parser.add_argument('-t', '--task', type=str, help='the task that you want to do. Possible options are `sentence` and `story_generate` and `story_analogy` ', required=True)
    parser.add_argument('-k', '--k', type=int, help='the times for story analogy generation', required=False, default=1)
    args=parser.parse_args()
    return args

if __name__ == '__main__': 
    args = parse_args()
    task = args.task
    key = config.GPT4KEY["API_KEY"]
    sent_data = pd.read_csv("sentences.csv")
    num_generation = args.k
    if task == "sentence":
        fields = ["Index", "Sentence1", "Sentence2", "Analogy"]
        filename = "sent_analogy.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in tqdm(enumerate(sent_data.values)):
                try:
                    correct_out = prompts.sentence_analogy(sent1, sent2)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise
                
                csvwriter.writerow({
                    "Index": i,
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Analogy": correct_out
                })

    elif task == "story_generate":
        fields =  ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2"]
        filename = "story_generation.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in tqdm(enumerate(sent_data.values)):
                try:
                    story1, style1 = prompts.story_diverse(sent1)
                    story2, style2 = prompts.story_diverse(sent2)
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
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2", "Analogy"]
        filename_input = "story_generation.csv"
        filename_output = "story_analogy.csv"

        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for row in tqdm(csvreader):
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                story1, story2 = row["Story1"], row["Story2"]
                style1, style2 = row["Style1"], row["Style2"]
                analogy_list = []
                for k in range(num_generation):
                    try:
                        correct_out = prompts.story_analogy(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise
                    analogy_items = convert_to_list(correct_out)
                    if not analogy_list: 
                        analogy_list = analogy_items
                        continue
                        
                    for item in analogy_items:
                        if not any(similarity_check(existing_item[0], item[0]) > 0.7 and similarity_check(existing_item[1], item[1]) > 0.7 for existing_item in analogy_list):
                            analogy_list.append(item)
                result = "\n".join(f"{i+1}. {item[0]} <-> {item[1]} | {item[2]}" for i, item in enumerate(analogy_list))
                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Story1": story1,
                    "Story2": story2,
                    "Style1": style1,
                    "Style2": style2,    
                    "Analogy": result
                })
    elif task == "name_generate":
        fields =  ["Index", "Sentence1", "Sentence2", "Story1", "Story2"]
        filename = "name_generation.csv"
        filename_story = "story_generation.csv"
        names1 = ["Jessica", "Jeffrey", "Elaine", "Will", "Gabriella", "Charles", "Rose", "Edward", "Sophia", "Dean", "Olivia", "Liam", "Madison", "Luke", "Zoe", "Evan"]
        names2 = ["Clara", "Samuel", "Nora", "Martin", "Bella", "Leo", "Amy", "Jared", "Rebecca", "Elias", "Eleanor", "Max", "Mila", "Owen", "Tara", "Jacob"]

        with open(filename, 'w', newline='') as csvfile, open(filename_story, 'r') as csvfile_input:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for row in tqdm(csvreader):
                try:
                    story1 = prompts.story_names(names1, row["Story1"])
                    story2 = prompts.story_names(names2, row["Story2"])
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise

                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": row["Sentence1"],
                    "Sentence2": row["Sentence2"],
                    "Story1": story1,
                    "Story2": story2
                })
    elif task == "name_analogy":
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Analogy"]
        filename_input = "name_generation.csv"
        filename_output = "name_analogy.csv"

        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for row in tqdm(csvreader):
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                story1, story2 = row["Story1"], row["Story2"]
                analogy_list = []
                for k in range(num_generation):
                    try:
                        correct_out = prompts.name_analogy(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise
                    analogy_items = convert_to_list(correct_out)
                    if not analogy_list: 
                        analogy_list = analogy_items
                        continue
                        
                    for item in analogy_items:
                        if not any(similarity_check(existing_item[0], item[0]) > 0.7 and similarity_check(existing_item[1], item[1]) > 0.7 for existing_item in analogy_list):
                            analogy_list.append(item)
                result = "\n".join(f"{i+1}. {item[0]} <-> {item[1]} | {item[2]}" for i, item in enumerate(analogy_list))
                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Story1": story1,
                    "Story2": story2,   
                    "Analogy": result
                })