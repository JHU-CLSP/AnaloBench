import csv
import spacy
import random
import prompts
import argparse
import itertools
import pandas as pd
from tqdm import tqdm

styles = ["Narrative", "Descriptive", "Expository", "Persuasive", "Creative", "Objective", "Subjective", "Review",
          "Poetry", "Technical"]
style_pairs = list(itertools.combinations(styles, 2))
pair_counts = {pair: 0 for pair in style_pairs}

# Load Spacy's English model
nlp = spacy.load('en_core_web_sm')


def parse_styles(fixed_style=None):
    selected_pair = None
    if fixed_style:
        eligible_pairs = [pair for pair in style_pairs if fixed_style == pair[0]]
        min_count = float('inf')
        for ep in eligible_pairs:
            if pair_counts[ep] < min_count:
                min_count = pair_counts[ep]
                selected_pair = ep
    else:
        min_count = min(pair_counts.values())
        eligible_pairs = [pair for pair, count in pair_counts.items() if count == min_count]
        selected_pair = random.choice(eligible_pairs)
    pair_counts[selected_pair] += 1

    return selected_pair


def similarity_check(text1, text2):
    doc1 = nlp(text1.lower())
    doc2 = nlp(text2.lower())

    tokens1 = [token.lemma_ for token in doc1]
    tokens2 = [token.lemma_ for token in doc2]

    # token overlap:
    overlap = len(set(tokens1).intersection(set(tokens2)))
    total_unique_words = len(set(tokens1).union(set(tokens2)))
    return overlap / total_unique_words


def convert_to_list(input_str):
    # Split the input string into a list of statements
    statements = input_str.split("\n")

    result = []

    # Loop through each statement
    for statement in statements:
        print(" --> statement: ", statement)
        delimiter = " | "
        if delimiter not in statement:
            continue
        paired_terms, explanation = statement.split(delimiter)
        delimiter = " <-> "
        if delimiter not in paired_terms:
            continue
        term1, term2 = paired_terms.split(delimiter)

        # Remove leading "- " from the first term
        term1 = term1[2:] if term1.startswith('- ') else term1

        result.append((term1, term2, explanation))

    assert len(result) > 0, f"No analogies found in {statements}!"

    return result


if __name__ == '__main__':

    # parse the arguments
    parser = argparse.ArgumentParser(description='Run the GPT-4 API. Use --help to see the options.')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `generate_sentence_analogies`: The script identifies analogies between the two provided sentences and writes them into a CSV file'
                             
                             '\n (2) `generate_stories`: The script generates diverse stories from the two provided sentences or stories and writes them into a CSV file '
                             '\n (3) `generate_story_analogies`: Runs a story analogy task that creates analogies between two stories multiple times based on the `-k` argument and writes them into a CSV file.'
                             
                             '\n (4) `generate_stories_with_names`: Reads story generations and assign names to the objects within the story, and writes the results into a CSV file.'
                             '\n (5) `generate_name_analogies`: Creates analogies between two stories with aligned names multiple times based on the `-k` argument and writes them into a CSV file. '
                             
                             '\n (6) `replace_story_mentions_with_random_words`: Generate stories that use random names as mentions. '
                             '\n (7) `generate_analogies_story_mentions_with_random_words`: Creates analogies between two stories that contain random names. The generation is done multiple times based on the `-k` argument and writes them into a CSV file. ',
                        required=True)
    parser.add_argument('--k', '-k', type=int, default=None,
                        help='The number of the repetitions we prompt the model for generating analogies.',
                        required=False)
    parser.add_argument('--num', '-n', type=int, default=None,
                        help='The number of instances to use for generation. ', required=False)

    args = parser.parse_args()
    task = args.task
    num_repetition = args.k
    num_generation = args.num

    if task == "generate_sentence_analogies":
        sent_data = pd.read_csv("data/sentences.csv")
        fields = ["Index", "Sentence1", "Sentence2", "Analogy"]
        filename = "data/1.sent_analogy.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in tqdm(enumerate(sent_data.values)):
                if i > num_generation:
                    break
                try:
                    correct_out = prompts.generate_analogies(sent1, sent2)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise

                csvwriter.writerow({
                    "Index": i,
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Analogy": correct_out
                })
    elif task == "generate_stories":
        sent_data = pd.read_csv("data/sentences.csv")
        processed_stories = {}
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2"]
        filename = "data/2.story_generation.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, (sent1, sent2) in tqdm(enumerate(sent_data.values)):
                if i > num_generation:
                    break
                try:
                    story1, story2, style1, style2 = None, None, None, None
                    if sent1 in processed_stories:
                        story1, style1 = processed_stories[sent1]
                        style1, style2 = parse_styles(style1)
                    else:
                        style1, style2 = parse_styles()
                        processed_stories[sent1] = (prompts.generate_diverse_story(sent1, style1), style1)
                        story1, style1 = processed_stories[sent1]
                    story2 = prompts.generate_diverse_story(sent2, style2)
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
    elif task == "generate_story_analogies":
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2", "Analogy"]
        filename_input = "data/2.story_generation.csv"
        filename_output = "data/3.story_analogy.csv"

        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for i, row in tqdm(enumerate(csvreader)):
                if i > num_generation:
                    break
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                story1, story2 = row["Story1"], row["Story2"]
                style1, style2 = row["Style1"], row["Style2"]
                analogy_list = []
                for k in range(num_repetition):
                    try:
                        correct_out = prompts.generate_analogies(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise
                    analogy_items = convert_to_list(correct_out)
                    if not analogy_list:
                        analogy_list = analogy_items
                        continue

                    for item in analogy_items:
                        if not any(
                                similarity_check(existing_item[0], item[0]) > 0.7 and similarity_check(existing_item[1],
                                                                                                       item[1]) > 0.7
                                for existing_item in analogy_list):
                            analogy_list.append(item)
                # sort the analogies alphabetically
                analogy_list = sorted(analogy_list, key=lambda x: x[0].lower())
                result = "\n".join(f"{item[0]} <-> {item[1]} | {item[2]}" for i, item in enumerate(analogy_list))
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
    elif task == "generate_stories_with_names":
        processed_stories = {}
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2"]
        filename = "data/4.name_generation.csv"
        filename_story = "data/2.story_generation.csv"
        names1 = ["Jessica", "Jeffrey", "Elaine", "Will", "Gabriella", "Charles", "Rose", "Edward", "Sophia", "Dean",
                  "Olivia", "Liam", "Madison", "Luke", "Zoe", "Evan"]
        names2 = ["Clara", "Samuel", "Nora", "Martin", "Bella", "Leo", "Amy", "Jared", "Rebecca", "Elias", "Eleanor",
                  "Max", "Mila", "Owen", "Tara", "Jacob"]

        with open(filename, 'w', newline='') as csvfile, open(filename_story, 'r') as csvfile_input:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()

            for i, row in tqdm(enumerate(csvreader)):
                if i > num_generation:
                    break
                try:
                    sent1 = row["Sentence1"]
                    if sent1 not in processed_stories:
                        processed_stories[sent1] = prompts.generate_stories_with_human_names(names1, row["Story1"])
                    story1 = processed_stories[sent1]

                    story2 = prompts.generate_stories_with_human_names(names2, row["Story2"])
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise

                style1 = row["Style1"]
                style2 = row["Style2"]

                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": row["Sentence1"],
                    "Sentence2": row["Sentence2"],
                    "Story1": story1,
                    "Story2": story2,
                    "Style1": style1,
                    "Style2": style2
                })
    elif task == "generate_name_analogies":
        fields = ["Index", "Sentence1", "Sentence2", "Story1", "Story2", "Style1", "Style2", "Analogy"]
        filename_input = "data/4.name_generation.csv"
        filename_output = "data/5.name_analogy.csv"

        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for i, row in tqdm(enumerate(csvreader)):
                if i > num_generation:
                    break
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                story1, story2 = row["Story1"], row["Story2"]
                style1, style2 = row["Style1"], row["Style2"]
                analogy_list = []
                for k in range(num_repetition):
                    try:
                        correct_out = prompts.extract_analogies_between_named_stories(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise
                    analogy_items = convert_to_list(correct_out)
                    if not analogy_list:
                        analogy_list = analogy_items
                        continue

                    for item in analogy_items:
                        if not any(
                                similarity_check(existing_item[0], item[0]) > 0.7 and similarity_check(existing_item[1],
                                                                                                       item[1]) > 0.7
                                for existing_item in analogy_list):
                            analogy_list.append(item)
                # sort the analogies alphabetically
                analogy_list = sorted(analogy_list, key=lambda x: x[0])
                result = "\n".join(f"{item[0]} <-> {item[1]} | {item[2]}" for i, item in enumerate(analogy_list))
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
    elif task == "replace_story_mentions_with_random_words":
        # replace the mentions in the story with random words

        fields = ["Index", "Sentence1", "Sentence2", "Original_Story1", "Original_Story2", "Style1", "Style2", "Story1", "Story2"]
        filename_input = "data/2.story_generation.csv"
        filename_output = "data/6.story_generation_random_names.csv"

        story_cache = {}
        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for i, row in tqdm(enumerate(csvreader)):
                if i > num_generation:
                    break
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                story1, story2 = row["Story1"], row["Story2"]
                style1, style2 = row["Style1"], row["Style2"]

                # sample 15 random mentions
                random_names_subset = ", ".join(random.sample(prompts.random_names(), 15))

                if story1 in story_cache:
                    new_story1 = story_cache[story1]
                else:
                    new_story1 = prompts.generate_stories_with_random_names(random_names_subset, row["Story1"])
                    story_cache[story1] = new_story1

                if story2 in story_cache:
                    new_story2 = story_cache[story2]
                else:
                    new_story2 = prompts.generate_stories_with_random_names(random_names_subset, row["Story2"])
                    story_cache[story2] = new_story2

                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Original_Story1": story1,
                    "Original_Story2": story2,
                    "Style1": style1,
                    "Style2": style2,
                    "Story1": new_story1,
                    "Story2": new_story2,
                })
    elif task == "generate_analogies_story_mentions_with_random_words":
        fields = ["Index", "Sentence1", "Sentence2", "Original_Story1", "Original_Story2", "Style1", "Style2", "Story1",
                  "Story2", "Analogy"]
        filename_input = "data/6.story_generation_random_names.csv"
        filename_output = "data/7.analogy_generation_random_names.csv"

        with open(filename_input, 'r') as csvfile_input, open(filename_output, 'w', newline='') as csvfile_output:
            csvreader = csv.DictReader(csvfile_input)
            csvwriter = csv.DictWriter(csvfile_output, fieldnames=fields)
            csvwriter.writeheader()

            for i, row in tqdm(enumerate(csvreader)):
                if i > num_generation:
                    break
                sent1, sent2 = row["Sentence1"], row["Sentence2"]
                original_story1, original_story2 = row["Original_Story1"], row["Original_Story2"]
                story1, story2 = row["Story1"], row["Story2"]
                style1, style2 = row["Style1"], row["Style2"]

                analogy_list = []
                for k in range(num_repetition):
                    try:
                        correct_out = prompts.generate_analogies(story1, story2)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        raise
                    analogy_items = convert_to_list(correct_out)
                    if not analogy_list:
                        analogy_list = analogy_items
                        continue

                    for item in analogy_items:
                        if not any(
                                similarity_check(existing_item[0], item[0]) > 0.7 and similarity_check(existing_item[1],
                                                                                                       item[1]) > 0.7
                                for existing_item in analogy_list):
                            analogy_list.append(item)
                # sort the analogies alphabetically
                analogy_list = sorted(analogy_list, key=lambda x: x[0].lower())
                result = "\n".join(f"{item[0]} <-> {item[1]} | {item[2]}" for i, item in enumerate(analogy_list))
                csvwriter.writerow({
                    "Index": row["Index"],
                    "Sentence1": sent1,
                    "Sentence2": sent2,
                    "Original_Story1": original_story1,
                    "Original_Story2": original_story2,
                    "Style1": style1,
                    "Style2": style2,
                    "Story1": story1,
                    "Story2": story2,
                    "Analogy": result
                })