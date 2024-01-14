import csv
import random
import argparse
import pandas as pd

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

def classification_base_generation(sentence_bank, clusters):
    # Define the header fields for the CSV.
    fields = ["Index", "Sentence", "Options", "Label"]

    # Create and write the header to the CSV file that will store the classification base data.
    with open('data/S-Base.csv', 'w') as f:
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
        with open('data/S-Base.csv', 'a') as f:
            csvwriter = csv.DictWriter(f, fieldnames=fields)
            csvwriter.writerow({
                'Index': i,
                'Sentence': sent,
                'Options': ",".join(str(num) for num in all_candidates),
                'Label': correct_label
            })
def classification_data_generation(task, story_clusters):
    fieldnames = ['Index', 'Sentence', "Story", "Options", "Label"]
    with open(f"data/S{task}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    # Load the dataset
    df = pd.read_csv('data/S-Base.csv')
    for i in range(len(df)):
        options = df["Options"][i].split(",")
        labels = ['A', 'B', 'C', 'D']
        options = "\n".join([f"{labels[j]}. {story_clusters[df['Sentence'][int(candidate)]]}" for j, candidate in enumerate(options)])
        with open(f"data/S{task}.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Story": story_clusters[df['Sentence'][i]], "Options": options, "Label": df['Label'][i]})



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate dataset for different tasks. Use --help to see the options.')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `generate_base_classification`: Generates a dataset that includes indices for options. This dataset serves as the foundational data for other tasks.'
                             '\n (2) `generate_s1_classification`: Builds a dataset tailored for single sentence classification tasks, utilizing the base dataset as an input.'
                             '\n (3) `generate_s10_classification`: Creates a dataset designed for classification tasks involving 10 sentences, also based on the initial dataset.'
                             '\n (4) `generate_s30_classification`: Produces a dataset aimed at classification tasks with 30 sentences, which similarly requires the preliminary dataset.'
                             '\n (5) `generate_base_retrieval`: Generates a dataset that includes indices for options. This dataset serves as the foundational data for other tasks.',
                        required=True)
    args = parser.parse_args()
    task = args.task
    if task == "generate_base_classification":
        sentence_bank, clusters, _ = load_and_map_clustered_sentences(0)
        classification_base_generation(sentence_bank, clusters)
    elif task == "generate_s1_classification":
        fieldnames = ['Index', 'Sentence', "Options", "Label"]
        with open("data/S1.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        # Load the dataset
        df = pd.read_csv('data/S-Base.csv')
        for i in range(len(df)):
            options = df["Options"][i].split(",")
            labels = ['A', 'B', 'C', 'D']
            options = "\n".join([f"{labels[j]}. {df['Sentence'][int(candidate)]}" for j, candidate in enumerate(options)])
            with open("data/S1.csv", "a") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({'Index': i, 'Sentence': df['Sentence'][i], "Options": options, "Label": df['Label'][i]})
    elif task == "generate_s10_classification":
        _, _, story_clusters = load_and_map_clustered_sentences(10)
        classification_data_generation(10, story_clusters)
    elif task == "generate_s30_classification":
        _, _, story_clusters = load_and_map_clustered_sentences(30)
        classification_data_generation(30, story_clusters)
    elif task == "generate_base_retrieval":
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
        
    