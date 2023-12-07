import pandas as pd
import os
import re

text_files_directory = r"testpytesseract\OCR\scb\ocr_text"

list_data = []

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

# Mapping datetime
def map_datetime(list_data):
    date = []
    time = []
    # pattern = re.compile(r'@.*สำเร็จ')

    for sublist in list_data:
        for idx, data in enumerate(sublist):
            if data.startswith('@') and levenshteinDistance(data[-6:], 'สำเร็จ') < 5:
                date_match = re.search(r'(.*)-', sublist[idx+1])
                if date_match:
                    date.append(date_match.group(1))
                # Use regex to extract string after '-'
                time_match = re.search(r'-(.*)', sublist[idx + 1])
                if time_match:
                    time.append(time_match.group(1))

    return len(date),len(time),date, time

def map_owner(list_data):
    owner_name = []
    owner_account = []
    for idxs,sublist in enumerate(list_data):
        for idx,data in enumerate(sublist):
            if data.startswith('รหัสอ้างอิง') or levenshteinDistance(data[:12], 'รหัสอ้างอิง') < 5:
                owner_name.append(sublist[idx + 1])
                if re.search(r'\d', sublist[idx + 2]):
                    owner_account.append(sublist[idx + 2])
                else:
                    owner_account.append(sublist[idx + 3])
                break

    return len(owner_name),len(owner_account),owner_name,owner_account

def map_recipient(list_data):
    recipient_name = []
    recipient_account = []
    idx_array = []
    pattern = re.compile(r'^[xX0-9—-]+$')

    for sublist in list_data:
        for idx,data in enumerate(sublist):
            if pattern.match(data):
                # print(idx,data)
                idx_array.append([idx,sublist[idx]])

        recipient_name.append(sublist[idx_array[0][0]+1])

        if len(idx_array) > 1:
            recipient_account.append(sublist[idx_array[1][0]])
        else:
            recipient_account.append("Not found")

        idx_array.clear()

    return len(recipient_name),recipient_name,len(recipient_account),recipient_account

def map_amount(list_data):
    amount = []
    for sublist in list_data:
        check_isHasAmount = False
        for idx,data in enumerate(sublist):
            if re.search(r'[0-9,]+\.[0-9]{2}', data):
                amount.append(sublist[idx])
                check_isHasAmount = True
                break
        if not check_isHasAmount:
            amount.append("Not found")

    return len(amount),amount

def map_memo(list_data):
    memo = []
    for sublist in list_data:
        check_isHasMemo = False
        for idx,data in enumerate(sublist):
            if data.startswith('บันทึกช่วยจำ') or levenshteinDistance(data[:12], 'บันทึกช่วยจำ') < 5:
                memo.append(sublist[idx+1])
                check_isHasMemo = True
                break
        if not check_isHasMemo:
            memo.append("Not found")
        
    return len(memo),memo



# Open file
for filename in os.listdir(text_files_directory):
    if filename.endswith('.txt'):
        with open(os.path.join(text_files_directory, filename), 'r', encoding='utf-8') as file:
            lines = file.readlines()
        list_data.append([line.strip() for line in lines if line.strip()])

# Show all data
# for idx,i in enumerate(list_data):
#     print(f"{idx} = {i}\n")

print(map_datetime(list_data))
print(map_owner(list_data))
print(map_recipient(list_data))
print(map_amount(list_data))
print(map_memo(list_data))
