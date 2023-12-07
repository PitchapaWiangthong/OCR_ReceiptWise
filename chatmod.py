import pandas as pd
import os
import re

# Regular expression patterns
pattern_only_Thai = r'[ก-๛]+'
pattern_start_Num = r'\d.*'
pattern_start_EngNumSpecial = r'[a-zA-Z0-9\\\/]+'
pattern_only_EngNum = r'[a-zA-Z0-9-]+'
pattern_only_ThaiEngNum = r'[ก-๛a-zA-Z0-9-.()]+'

def read_text_files(text_files_directory):
    list_data = []
    for filename in os.listdir(text_files_directory):
        if filename.endswith('.txt'):
            with open(os.path.join(text_files_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                # Define a regular expression pattern to capture data within single quotes
                pattern = r"'(.*?)'"
                # Find all matches of the pattern in the content
                matches = re.findall(pattern, content)
                # Append the matches to the 'list_data' list
                list_data.append(matches)
    return list_data

def extract_bank_account(data):
    return [item[0] for item in data]

def extract_dates(data):
    dates = []
    for item in data:
        thai_word = re.findall(pattern_only_Thai, item[1])
        if len(thai_word) != 1:
            dates.extend(re.findall(pattern_start_Num, item[1]))
    return dates

def extract_reference(data):
    references = []
    for item in data:
        ref = re.findall(pattern_start_EngNumSpecial, item[2])
        new_ref = ''.join(ref)
        references.append(new_ref)
    return references

def extract_sender_info(data):
    sender_names = [re.findall(pattern_only_Thai, item[4]) for item in data]
    sender_account_numbers = [re.findall(pattern_only_EngNum, item[4]) for item in data]
    return sender_names, sender_account_numbers

def extract_recipient_info(data):
    recipient_info = []
    for item in data:
        info = re.findall(pattern_only_ThaiEngNum, item[6])
        recipient_info.append(info)
    return recipient_info

if __name__ == "__main__":
    text_files_directory = 'test'

    # Read and process text files
    list_data = read_text_files(text_files_directory)
    
    # Extract data
    bank_accounts = extract_bank_account(list_data)
    dates = extract_dates(list_data)
    references = extract_reference(list_data)
    sender_names, sender_account_numbers = extract_sender_info(list_data)
    recipient_info = extract_recipient_info(list_data)

    print(bank_accounts)
    print(dates)
    print(references)
    print(sender_names)
    print(sender_account_numbers)
    print(recipient_info)

    # Further processing for recipient_info can be added here

    # Print or use the extracted data as needed
