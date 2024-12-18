import csv
import random
import argparse
import pandas as pd
from itertools import permutations

def load_and_map_clustered_sentences(task):
    # Load the dataset
    df = pd.read_csv('data/clusters.tsv', delimiter='\t')

    # Initialize an empty list to store all sentences
    sentence_bank = []

    # Initialize an empty dictionary to store cluster index to sentences mapping
    clusters = {}

    # Populate sentence_bank and clusters dictionary
    for cluster_index, group in df.groupby('cluster'):
        sentences = group['sentence'].tolist()
        sentence_bank.extend(sentences)
        for sentence in sentences:
            # Exclude the current sentence when adding neighbors
            clusters[sentence] = [neighbor for neighbor in sentences if neighbor != sentence]

    story_clusters = {}

    if task != 0:
        with open(f'data/stories-{task}.csv', 'r') as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                story_clusters[row[1]] = row[2]
    return sentence_bank, clusters, story_clusters

def t1_subset_base_generation(sentence_bank, clusters):
    # Define the header fields for the CSV.
    fields = ["Index", "Sentence", "Options", "Label"]

    # Create and write the header to the CSV file that will store the classification base data.
    with open('data/AnaloBench-T1-Subset-Base.csv', 'w') as f:
        csvwriter = csv.DictWriter(f, fieldnames=fields)
        csvwriter.writeheader()

    # Loop through each sentence in the sentence bank to create the classification data.
    for i in range(len(sentence_bank)):
        sent = sentence_bank[i]

        # Randomly choose a correct answer from the same cluster as the current sentence.
        true_candidate = sentence_bank.index(random.choice(clusters[sent]))

        # Randomly select three incorrect answers from sentences not in the same cluster.
        false_candidates = random.sample([index for index, item in enumerate(sentence_bank) if item not in clusters[sent]], 3)

        # Combine the correct and incorrect answers into a list of candidates for the options.
        all_candidates = false_candidates + [true_candidate]
        random.shuffle(all_candidates)  # Shuffle to randomize the order of the options.

        # Create labels for each of the four options: 'A', 'B', 'C', 'D'.
        labels = ['A', 'B', 'C', 'D']
        # Find the label corresponding to the correct option.
        correct_label = labels[all_candidates.index(true_candidate)]

        # Write the classification data for the current sentence to the CSV file.
        with open('data/AnaloBench-T1-Subset-Base.csv', 'a') as f:
            csvwriter = csv.DictWriter(f, fieldnames=fields)
            csvwriter.writerow({
                'Index': i,
                'Sentence': sent,
                'Options': ",".join(str(num) for num in all_candidates),
                'Label': correct_label
            })

def t1_full_base_generation(sentence_bank, clusters):
    fields = ["Index", "Sentence", "Options", "CorrectIndex", "Label"]

    index_counter = 0 

    with open('data/AnaloBench-T1-Full-Base.csv', 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        
        for sent, neighbors in clusters.items():
            # for each sentence, generate all unique pairs within its cluster
            for neighbor_sent in neighbors:
                true_candidate = sentence_bank.index(neighbor_sent)
                false_candidates = random.sample([index for index, item in enumerate(sentence_bank) if item not in [sent] + clusters[sent]], 3)
                all_candidates = false_candidates + [true_candidate]
                random.shuffle(all_candidates)
                labels = ['A', 'B', 'C', 'D']
                correct_label = labels[all_candidates.index(true_candidate)]
                    
                csvwriter.writerow({
                    'Index': index_counter,
                    'Sentence': sent,
                    'Options': ",".join(str(num) for num in all_candidates),
                    "CorrectIndex": true_candidate,
                    'Label': correct_label
                })
                index_counter += 1 

def t1_data_generation(task, story_clusters, size, sentence_bank):
    fieldnames = ['Index', 'Sentence', "Story", "Options", "Label"]
    with open(f"data/AnaloBench-T1-{size}-S{task}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    # Load the dataset
    if size == "subset":
        df = pd.read_csv('data/AnaloBench-T1-Subset-Base.csv')
    else:
        df = pd.read_csv('data/AnaloBench-T1-Full-Base.csv')
    for i in range(len(df)):
        options = df["Options"][i].split(",")
        labels = ['A', 'B', 'C', 'D']
        options = "\n".join([f"{labels[j]}. {story_clusters[sentence_bank[int(candidate)]]}" for j, candidate in enumerate(options)])
        with open(f"data/AnaloBench-T1-{size}-S{task}.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Story": story_clusters[df['Sentence'][i]], "Options": options, "Label": df['Label'][i]})

def t2_data_generation(task, story_clusters):
    fields = ["Index", "Sentence", "Options", "Indices"]
    with open(f"AnaloBench-T2-S{task}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
    # Load the dataset
    df = pd.read_csv('AnaloBench-T2-Base.csv')
    for i in range(len(df)):
        options = df["Options"][i].split(",")
        options =  [f"{i+1}. {story_clusters[sentence_bank[int(option)]]}" for i, option in enumerate(options)]
        with open(f"AnaloBench-T2-S{task}.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Story": story_clusters[df['Sentence'][i]], "Options": "\n".join(options), "Indices": df['Indices'][i]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate dataset for different tasks. Use --help to see the options.')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `generate_t1_base_subset`: Generates a subset dataset that includes indices for options. This dataset serves as the foundational data for other tasks.'
                             '\n (2) `generate_t1_base_full`: Generates a full dataset that includes indices for options. This dataset serves as the foundational data for other tasks.'
                             '\n (3) `generate_t1_s1`: Builds a dataset tailored for single sentence t1 tasks, utilizing the base dataset as an input.'
                             '\n (4) `generate_t1_s10`: Creates a dataset designed for t1 tasks involving 10 sentences, also based on the initial dataset.'
                             '\n (5) `generate_t1_s30`: Produces a dataset aimed at t1 tasks with 30 sentences, which similarly requires the preliminary dataset.'
                             '\n (6) `generate_t2_base`: Generates a dataset that includes indices for options. This dataset serves as the foundational data for other tasks.'
                             '\n (7) `generate_t2_s1`: Builds a dataset tailored for single sentence t2 tasks, utilizing the base dataset as an input.'
                             '\n (8) `generate_t2_s10`: Creates a dataset designed for t2 tasks involving 10 sentences, also based on the initial dataset.'
                             '\n (9) `generate_t2_s30`: Produces a dataset aimed at t2 tasks with 30 sentences, which similarly requires the preliminary dataset.',
                        required=True)
    parser.add_argument('--size', '-s', type=str, default=None,
                        help='The set of task that you want to do. Possible options are the following: '
                             '\n (1) `subset`: Generates a subset dataset around 340 samples.'
                             '\n (2) `full`: Generates a full dataset.')
    args = parser.parse_args()
    task = args.task
    size = args.size
    if task == "generate_t1_base_subset":
        sentence_bank, clusters, _ = load_and_map_clustered_sentences(0)
        t1_subset_base_generation(sentence_bank, clusters)
    elif task == 'generate_t1_base_full':
        sentence_bank, clusters, _ = load_and_map_clustered_sentences(0)
        t1_full_base_generation(sentence_bank, clusters)
    elif task == "generate_t1_s1":
        fieldnames = ['Index', 'Sentence', "Options", "Label"]
        with open(f"data/AnaloBench-T1-{size}-S1.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        # Load the dataset
        if size == "subset":
            df = pd.read_csv('data/AnaloBench-T1-Subset-Base.csv')
        else:
            df = pd.read_csv('data/AnaloBench-T1-Full-Base.csv')
        sentence_bank, _, _ = load_and_map_clustered_sentences(0)
        for i in range(len(df)):
            options = df["Options"][i].split(",")
            labels = ['A', 'B', 'C', 'D']
            options = "\n".join([f"{labels[j]}. {sentence_bank[int(candidate)]}" for j, candidate in enumerate(options)])
            with open(f"data/AnaloBench-T1-{size}-S1.csv", "a") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Options": options, "Label": df['Label'][i]})
    elif task == "generate_t1_s10":
        sentence_bank, _, story_clusters = load_and_map_clustered_sentences(10)
        t1_data_generation(10, story_clusters, size, sentence_bank)
    elif task == "generate_t1_s30":
        sentence_bank, _, story_clusters = load_and_map_clustered_sentences(30)
        t1_data_generation(30, story_clusters, size, sentence_bank)
    elif task == "generate_t2_base":
        size_of_sentencebank = 200
        fields = ["Index", "Sentence", "Options", "Indices"]
        sentence_bank, clusters, _ = load_and_map_clustered_sentences(0)
        with open('data/R-Base.csv', 'w') as f:
            csvwriter = csv.DictWriter(f, fieldnames=fields)
            csvwriter.writeheader()
        for index, (key, value) in enumerate(clusters.items()):
            cluster = [key] + value
            tmp_bank = list(sentence_bank.copy())
            candidate = list(set(tmp_bank) - set(cluster))
            number_of_sentences = size_of_sentencebank - len(value)
            candidate = random.sample(candidate, number_of_sentences)
            tmp_bank = value + candidate
            random.shuffle(tmp_bank)
            sheet_bank = [sentence_bank.index(i) for i in tmp_bank]
            indices = [tmp_bank.index(elem)+1 for elem in cluster if elem in tmp_bank and elem != key]
            labeled_options = [f"{i+1}. {option}" for i, option in enumerate(tmp_bank)]
            s_sentence_bank = "\n".join(labeled_options)
            with open('data/R-Base.csv', 'a') as f:
                csvwriter = csv.DictWriter(f, fieldnames=fields)
                csvwriter.writerow({'Index': index, 'Sentence': key, 'Options': ",".join([str(index) for index in sheet_bank]), "Indices": ",".join([str(index) for index in indices])})
    elif task == "generate_t2_s1":
        fields = ["Index", "Sentence", "Options", "Indices"]
        with open("AnaloBench-T2-S1.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
        # Load the dataset
        df = pd.read_csv('AnaloBench-T2-Base.csv')
        for i in range(len(df)):
            options = df["Options"][i].split(",")
            options =  [f"{i+1}. {sentence_bank[int(option)]}" for i, option in enumerate(options)]
            with open("AnaloBench-T2-S1.csv", "a") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Options": "\n".join(options), "Indices": df['Indices'][i]})

    elif task == "generate_t2_s10": 
        _, _, story_clusters = load_and_map_clustered_sentences(10)
        t2_data_generation(10, story_clusters)

    elif task == "generate_t2_s30":
        _, _, story_clusters = load_and_map_clustered_sentences(30)
        t2_data_generation(30, story_clusters)
    