import re

text = "Your text with x123 and 456x and x789x and กขค and 987 and yxz."

# Define a regular expression pattern to match the desired string
pattern = r'[0-9x]+(?:[^ก-๙]+|$)'

# Use re.search to find the first match in the text
match = re.search(pattern, text)

if match:
    extracted_string = match.group()
    print(extracted_string)
else:
    print("String not found.")
