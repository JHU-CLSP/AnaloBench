import re
import os
import csv
import argparse
import pandas as pd
# Mean Average Precision
def calculate_average_precision(golden_list, result_list):
    relevance = [1 if sentence in golden_list else 0 for sentence in result_list]
    precision_at_i = 0
    num_relevant_items = 0
    sum_precision = 0

    for i, is_relevant in enumerate(relevance):
        if is_relevant:
            num_relevant_items += 1
            precision_at_i = num_relevant_items / (i + 1)
            sum_precision += precision_at_i

    average_precision = sum_precision / len(golden_list) if golden_list else 0
    return average_precision

def precision_at_k(golden, result, k):
    if k > len(result):
        raise ValueError("k should not be greater than the length of the result list.")

    # Get the top-k items from the result list
    top_k = set(result[:k])

    # Count the number of relevant items in the top-k results
    relevant_and_recommended = top_k.intersection(set(golden))
    number_relevant_and_recommended = len(relevant_and_recommended)

    # Precision at k is the ratio of relevant items in the top k
    precision = number_relevant_and_recommended / k
    return precision

def retrieval_at_k(golden, result, k):
    if k > len(result):
        raise ValueError("k should not be greater than the length of the result list.")

    # Get the top-k items from the result list
    top_k = set(result[:k])

    # Count the number of relevant items in the top-k results
    relevant_in_top_k = top_k.intersection(set(golden))
    number_relevant_in_top_k = len(relevant_in_top_k)

    # Count the total number of relevant items
    total_relevant = len(golden)

    # Retrieval at k is the ratio of relevant items in the top k to the total number of relevant items
    retrieval = number_relevant_in_top_k / total_relevant if total_relevant > 0 else 0
    return retrieval

def mean_reciprocal_rank(golden, result):
    golden_set = set(golden)
    reciprocal_ranks = []

    for i, item in enumerate(result):
        if item in golden_set:
            # We add 1 to the index because ranks are 1-based, not 0-based.
            reciprocal_rank = 1.0 / (i + 1)
            reciprocal_ranks.append(reciprocal_rank)
            break  # We only consider the first relevant item.
    # Compute the mean of the reciprocal ranks
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0
    return mrr

if __name__ == '__main__':

    # Load the dataset
    available = ["R30-GPT4.csv", "R10-GPT4.csv", "R1-GPT4.csv"]
    folder_path = 'data'  # Replace with your folder path
    all_results = []

    parser = argparse.ArgumentParser(description='Retrival Task Metircs. Use --help to see the options.')
    parser.add_argument('--task', '-t', type=str, default=None,
                        help='The task that you want to do. Possible options are the following: '
                             '\n (1) `MAP`: Mean Average Precision'
                             '\n (2) `Precision`: Precision@k'
                             '\n (3) `Retrieval`: Retrieval@k'
                             '\n (4) `MRR`: Mean Reciporal Rank',
                        required=True)
    parser.add_argument('--k', type=int, default=None,
                        help='The k parameter for P@k and R@k: ')
    args = parser.parse_args()
    task = args.task
    k = args.k
    func = None
    if task == "MAP":
        func = calculate_average_precision
    elif task == "Precision":
        func = precision_at_k
    elif task == "Retrieval":
        func = retrieval_at_k
    elif task == "MRR":
        func = mean_reciprocal_rank

    for filename in os.listdir(folder_path):
        # Check if the file is a CSV and exclude some base datasets
        if filename in available:
            file_path = os.path.join(folder_path, filename)
            results = []
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    golden = [int(i) for i in row['Indices'].split(",")]
                    try:
                        result = [int(i.rstrip(". \n\t")) for i in row['Result'].split(",")]

                        if task == "Precision" or task == "Retrieval":
                            results.append(func(golden, result, k))
                        else:
                            results.append(func(golden, result))
                    except Exception as e:
                        # print(e)
                        # print(row['Result'])
                        continue
                print(f"Task: {task}, Data: {filename}, Score: {sum(results)/len(results)}")