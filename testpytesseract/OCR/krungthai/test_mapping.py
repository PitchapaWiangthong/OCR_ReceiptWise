import pandas as pd
import os
import re

text_files_directory = r"testpytesseract\OCR\krungthai\ocr_text"

list_data = []
pattern_account_number = re.compile(r'^[×xX\d—-]+$')


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

    for sublist in list_data:
        for idx, data in enumerate(sublist):
            if data.startswith('วันที่') or (levenshteinDistance(data[:14], 'วันที่ทำรายการ') < 5):
                date_match = re.search(r'(\d+)(.*?)(?=-)',data)
                date.append(date_match.group(0))
                time_match = re.search(r'(?<=-)(.*)', data)
                time.append(time_match.group(0))

    return len(date),len(time),date,time

def map_owner(list_data):
    owner_name = []
    owner_account = []
    for idxs,sublist in enumerate(list_data):
        for idx,data in enumerate(sublist):
            if data == 'กรุงไทย' or levenshteinDistance(data, 'กรุงไทย') < 5:
                if len(sublist[idx - 1]) > 6:
                    owner_name.append(sublist[idx - 1])
                else:
                    owner_name.append(sublist[idx - 2])
            if pattern_account_number.match(data):
                owner_account.append(data)
                break


        
    return len(owner_name),len(owner_account),owner_name,owner_account

def map_recipient(list_data):
    recipient_name = []
    recipient_account = []
    idx_array = []

    for sublist in list_data:
        for idx, data in enumerate(sublist):
            if pattern_account_number.match(data):
                # print(idx,data)
                idx_array.append([idx,sublist[idx]])

        if len(sublist[idx_array[0][0] + 1]) > 6:
            if levenshteinDistance(sublist[idx_array[0][0] + 1][-6:], 'สำเร็จ') < 5:
                if len(sublist[idx_array[0][0] + 3]) < 6 :
                    recipient_name.append(sublist[idx_array[0][0] + 4])
                else:
                    recipient_name.append(sublist[idx_array[0][0] + 3])
            else:
                recipient_name.append(sublist[idx_array[0][0] + 1])
            
        else:
            recipient_name.append(sublist[idx_array[0][0] + 2])

        if len(idx_array) > 1:
            recipient_account.append(sublist[idx_array[1][0]])
        else:
            recipient_account.append("")

        idx_array.clear()

    return len(recipient_name),len(recipient_account),recipient_name,recipient_account


def map_amount(list_data):
    amount = []
    for sublist in list_data:
        for idx, data in enumerate(sublist):
            if (data.startswith('จำนวน') or (levenshteinDistance(data[:10], 'จำนวนเงิน') < 5)) and re.search(r'\d', data):
                amount_match = re.search(r'\d.*\d', data)
                if amount_match:
                    amount.append(amount_match.group(0))
                else:
                    amount.append("")
    return len(amount),amount

def map_memo(list_data):
    memo = []

    for sublist in list_data:
        if sublist[-1].startswith('วันที่') or (levenshteinDistance(sublist[-1][:14], 'วันที่ทำรายการ') < 5):
            memo.append("")
        else:
            if len(sublist[-1]) > 5:
                memo.append(sublist[-1])
        
    return len(memo),memo


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
print(map_owner(list_data))
print(map_recipient(list_data))
print(map_amount(list_data))
print(map_memo(list_data))
