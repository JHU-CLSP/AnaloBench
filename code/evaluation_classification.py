import re
import os
import csv
import pandas as pd
def check_out(filename, results):
    pattern = r'(?:\:\s)?([A-D])(?:\.|\s|$)'
    correct = 0
    wrong = 0
    irrelvant = 0
    for r, l in results:
        r = str(r)
        tmp = list(set(re.findall(pattern, r)))
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

if __name__ == '__main__':

    # Load the dataset
    exclude_set = ["S-Base.csv", "S1.csv", "S10.csv", "S30.csv", "stories-10.csv", "stories-30.csv", "R30-GPT4.csv", "R10-GPT4.csv", "R1-GPT4.csv", "R-Base.csv"]
    folder_path = 'data'  # Replace with your folder path
    all_results = []

    for filename in os.listdir(folder_path):
        # Check if the file is a CSV and exclude some base datasets
        if filename.endswith('.csv') and filename not in exclude_set:
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            try:
                all_results.append(check_out(filename, list(zip(df["Result"], df["Label"]))))
            except Exception as e:
                print(filename)
                print(e)
                break