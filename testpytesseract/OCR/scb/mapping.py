import pandas as pd
import os
import re
import json

text_files = r"testpytesseract\OCR\scb\ocr_text\ocr_result_TXN_202308309zFEXC50bixHCgc3M.jpg.txt"
list_data = []
recipient_account = ''
recipient_name = ''
memo = ''

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

def remove_word_from_string(input_string, words_to_remove):
    # Create a regular expression pattern to match the word with optional whitespace
    for word_to_remove in words_to_remove:
        pattern = re.compile(fr'(?:{"|".join(map(re.escape, words_to_remove))})\s*')
        # Use the pattern to replace the matched word with an empty string
        modified_string = re.sub(pattern, '', input_string)

    return modified_string

# Example usage:
# original_string = "จาก@บเายกฤษฎาสารอิทย์"
# words_to_remove = ["จาก","@"]
# result = remove_word_from_string(original_string, words_to_remove)
# print(result)


with open(os.path.join(text_files), 'r', encoding='utf-8') as file:
    lines = file.readlines()
    list_data.extend([line.strip() for line in lines if line.strip()])
print(list_data)

pattern_account_number = re.compile(r'^[×xX\d—-]+$')

levels = 0

for idx,data  in enumerate(list_data):

    # map date time
    if data.startswith('@') and (levenshteinDistance(data[-6:], 'สำเร็จ') < 5) and levels == 0:
        date_match = re.search(r'(.*)-', list_data[idx+1])
        if date_match:
            date = date_match.group(1)
        else:
                date = ""
        # Use regex to extract string after '-'
        time_match = re.search(r'-(.*)', list_data[idx + 1])
        if time_match:
            time= time_match.group(1)
        else:
                time = ""
        levels += 1

    # map name , account owner
    if (data.startswith('รหัสอ้างอิง') or levenshteinDistance(data[:12], 'รหัสอ้างอิง') < 5) and levels == 1:
        words_to_remove = ["จาก","@"]
        owner_name = remove_word_from_string(list_data[idx + 1], words_to_remove)

        if re.search(r'\d', list_data[idx + 2]):
            owner_account = list_data[idx + 2]
        else:
            owner_account = list_data[idx + 3]
            
        levels += 1

    if pattern_account_number.match(data) and recipient_name != "":
        recipient_account = list_data[idx]

    if pattern_account_number.match(data) and levels == 2:
        words_to_remove = ["ไปยัง","@"]
        recipient_name = remove_word_from_string(list_data[idx + 1], words_to_remove)
        levels += 1

    if levels == 3:
        amount = re.search(r'[0-9,]+\.[0-9]{2}', data)
        if amount != None:
            amount = amount.group(0)
            levels += 1
    
    if levels == 4:
        if data.startswith('บันทึกช่วยจำ') or levenshteinDistance(data[:12], 'บันทึกช่วยจำ') < 5:
            memo = list_data[idx+1]
            break
        else:
            memo = ""
    
    
jsonData = {
    "date": date,
    "time": time,
    "owner_name" : owner_name,
    "owner_account" : owner_account,
    "recipient_name" : recipient_name,
    "recipient_account" : recipient_account,
    "amount" : amount,
    "memo" : memo
}
json_data = json.dumps(jsonData,ensure_ascii=False, indent=2)
print(json_data)