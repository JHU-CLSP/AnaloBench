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
        if len(tmp) == 0:
            irrelvant += 1
        else:
            if tmp[0] == l:
                correct += 1
            else:
                wrong += 1
    print(f'FileNmae: {filename}')
    print(f'Correct: {correct}, Wrong: {wrong}, Irrelevant: {irrelvant}, Total: {correct + wrong + irrelvant}')
    print(f'Accuracy: {(correct + irrelvant * 0.25)/ len(results)}')
    return (filename, [correct, wrong, irrelvant])

if __name__ == '__main__':

    # Load the dataset
    folder_path = 'result'  # Replace with your folder path
    all_results = []

    for filename in os.listdir(folder_path):
        # Check if the file is a CSV
        if "T1" in filename and filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            try:
                all_results.append(check_out(filename, list(zip(df["Result"], df["Label"]))))
            except Exception as e:
                print(filename)
                print(e)
                break