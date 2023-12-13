import pandas as pd
import os
import re
import json

text_files_directory = r"testpytesseract\OCR\kbank\ocr_text"

list_data = []
pattern_account_number = re.compile(r'^[×xX%\d—-]+$')

# levenshteinDistance
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_

    return distances[-1]

def map_datetime(list_data):
    date = []
    time = []


# Open file
for filename in os.listdir(text_files_directory):
    if filename.endswith('.txt'):
        with open(os.path.join(text_files_directory, filename), 'r', encoding='utf-8') as file:
            lines = file.readlines()
        list_data.append([line.strip() for line in lines if line.strip()])

# # Show all data
# for idx,i in enumerate(list_data):
#     print(f"{idx} = {i}\n")

print(map_datetime(list_data))
# print(map_owner(list_data))
# print(map_recipient(list_data))
# print(map_amount(list_data))
# print(map_memo(list_data))