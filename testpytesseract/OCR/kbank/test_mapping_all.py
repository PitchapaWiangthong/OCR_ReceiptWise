import os
import re
import json

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

# Specify the folder containing .txt files
folder_path = r"testpytesseract\OCR\kbank\ocr_text"

# Specify the result file path
result_file_path = r"testpytesseract\OCR\kbank\result_OCR.txt"

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            list_data = [line.strip() for line in lines if line.strip()]

        pattern_account_number = re.compile(r'[Xx×%—-]+[\d—-]+')
        recipient_account = ''
        recipient_name = ''
        owner_account = ''
        owner_name = ''
        amount = ''
        memo = ''
        levels = 0
        amount_set = []

        for idx,data  in enumerate(list_data):
                
            if levels == 0:
                date = list_data[idx+1]
                levels += 1

            if (levenshteinDistance(data, 'ธ.กสิกรไทย') < 5) and levels == 1:
                if len(list_data[idx - 1]) > 6:
                    owner_name = list_data[idx - 1]
                owner_account = list_data[idx + 1]
                if len(list_data[idx + 2]) > 6:
                    recipient_name = list_data[idx + 2]
                else:
                    recipient_name = list_data[idx + 3]
                levels += 1
                continue

            if pattern_account_number.match(data) and levels == 2:
                recipient_account = data
                if owner_account == recipient_account:
                    recipient_account = ''
                    continue
                levels += 1

            amount_match = re.search(r'[\d]+[.][\d]+', data)
            
            if amount_match:
                amount_set.append(data)

            if len(amount_set) > 0:
                if len(amount_set) > 2 and amount_set[0] == date:
                    amount_match = re.search(r'\d.*\d', amount_set[1])
                    amount = amount_match.group(0)
                else:
                    amount_match = re.search(r'\d.*\d', amount_set[0])
                    amount = amount_match.group(0)

            if data.startswith('บันทึกช่วยจำ') or (levenshteinDistance(data[:12], 'บันทึกช่วยจำ') < 5):
                memo_match = remove_word_from_string(data,'บันทึกช่วยจํา:')
                memo = memo_match


        jsonData = {
            "date": date,
            # "time": time,
            "owner_name" : owner_name,
            "owner_account" : owner_account,
            "recipient_name" : recipient_name,
            "recipient_account" : recipient_account,
            "amount" : amount,
            "memo" : memo,
        }
        json_data = json.dumps(jsonData,ensure_ascii=False, indent=2)
        print(json_data)

        # Write the output to the result file
        with open(result_file_path, 'a', encoding='utf-8') as result_file:
            result_file.write(json_data + '\n') 

print(f"Results have been written to {result_file_path}")