import os
import csv
import pandas as pd
import re

def check_out(filename, results):
    pattern = r'\s?([A-Z])\.'
    correct = 0
    wrong = 0
    irrelvant = 0
    for r, l in results:
        r = str(r)
        if len(r) == 1:
            if l == r:
                correct += 1
            else:
                wrong += 1
        else:
            tmp = re.findall(pattern, r)
            if len(tmp) == 1:
                if tmp[0] == l:
                    correct += 1
                else:
                    wrong += 1
            else:
                irrelvant += 1
    print(f'FileNmae: {filename}')
    print(f'Correct: {correct}, Wrong: {wrong}, Irrelevant: {irrelvant}, Total: {correct + wrong + irrelvant}')
    print(f'Accuracy: {(correct + irrelvant * 0.25)/ len(results)}')
    return (filename, [correct, wrong, irrelvant])
    
# Load the dataset
folder_path = 'results'  # Replace with your folder path
all_results = []

for filename in os.listdir(folder_path):
    # Check if the file is a CSV and not "story-10.csv"
    if filename.endswith('.csv') and filename != "stories-10.csv":
        file_path = os.path.join(folder_path, filename)
        dtype_dict = {
            'Result': str,
            'Label': str
        }
        df = pd.read_csv(file_path, dtype=dtype_dict)
        try:
            all_results.append(check_out(filename, list(zip(df["Result"], df["Label"]))))
        except Exception as e:
            print(filename)
            print(e)
            break