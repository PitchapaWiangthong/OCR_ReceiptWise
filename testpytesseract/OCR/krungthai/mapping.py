import pandas as pd
import os
import re
import json

text_files = r"testpytesseract\OCR\krungthai\ocr_text\ocr_result_IMG_1818.PNG.txt"
list_data = []
recipient_account = ''
recipient_name = ''
owner_account = ''
amount = ''
memo = ''
levels = 0

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

with open(os.path.join(text_files), 'r', encoding='utf-8') as file:
    lines = file.readlines()
    list_data.extend([line.strip() for line in lines if line.strip()])
print(list_data)

pattern_account_number = re.compile(r'^[×xX%\d—-]+$')

levels = 0

for idx,data  in enumerate(list_data):

    if data.startswith('วันที่') or (levenshteinDistance(data[:14], 'วันที่ทำรายการ') < 5) and levels == 0:
        date_match = re.search(r'(\d+)(.*?)(?=-)',data)
        date = date_match.group(0)
        time_match = re.search(r'(?<=-)(.*)', data)
        time = time_match.group(0)

        levels += 1

    if (data == 'กรุงไทย' or levenshteinDistance(data, 'กรุงไทย') < 5):
        if len(list_data[idx - 1]) > 6:
            owner_name = list_data[idx - 1]
        else:
            owner_name = list_data[idx - 2]

        levels += 1

    if pattern_account_number.match(data) and levels == 1:
        owner_account = data
        if len(list_data[idx + 1]) > 6:
            if levenshteinDistance(list_data[idx + 1][-6:],'สำเร็จ') < 5:
                if len(list_data[idx + 3]) < 6:
                    recipient_name = list_data[idx + 4]
                else:
                    recipient_name = list_data[idx + 3]
            else:
                recipient_name = list_data[idx + 1]
        else:
            recipient_name = list_data[idx + 2]

        levels += 1
        continue

    pattern = re.compile(r'[×xX]+')
    if len(pattern.findall(data)) > 0:
        # print(pattern_account_number.findall(data))
        recipient_account_match = re.search(r'[Xx×%—-]+[\d—-]+',data)
        recipient_account = recipient_account_match.group(0)

    if data == 'พร้อมเพย์' or levenshteinDistance(data, 'พร้อมเพย์') < 5:
        recipient_account = list_data[idx + 1]
        
    if (data.startswith('จำนวน') or (levenshteinDistance(data[:10], 'จำนวนเงิน') < 5)) and re.search(r'\d', data):
        amount_match = re.search(r'\d.*\d', data)
        if amount_match:
            amount = amount_match.group(0)
        else:
            amount = ""


    if data.startswith('วันที่') or (levenshteinDistance(data[:14], 'วันที่ทำรายการ') < 5):
        memo = ""
    else:
        if len(data) > 5:
            if levenshteinDistance(data[:13], 'บันทึกช่วยจำ]') < 5:
                memo = data[13:]
            else:
                memo = data

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