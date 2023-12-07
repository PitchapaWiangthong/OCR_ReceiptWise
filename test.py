import pandas as pd
import os
import re

text_files_directory = 'test'
df = pd.DataFrame()
list_data = []

for filename in os.listdir(text_files_directory):
    if filename.endswith('.txt'):
        with open(os.path.join(text_files_directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Define a regular expression pattern to capture data within single quotes
            pattern = r"'(.*?)'"

            # Find all matches of the pattern in the content
            matches = re.findall(pattern, content)
            
            # Append the matches to the 'data' list
            list_data.append(matches)


#pattern
pattern_only_Thai = r'[ก-๛]+'
pattern_start_Num = r'\d.*'
pattern_start_EngNumSpecial = r'[a-zA-Z0-9\\\/]+'
pattern_only_EngNum = r'[a-zA-Z0-9-]+'
pattern_only_ThaiEngNum = r'[ก-๛a-zA-Z0-9-.()]+'

#extract bank account
bank = []
for i in list_data:
    bank.append(i[0])
# print(len(bank))
# print(bank)

#extract date
dates = [] 
for i in list_data:
    thaiWord = re.findall(pattern_only_Thai,i[1])               
    if len(thaiWord) == 1:
        i.pop(1)
    dates.extend(re.findall(pattern_start_Num, i[1]))
# print(len(dates))
# print(dates)
# for date in dates:
#     print(date)

#extract reference
reference = []

for i in list_data:
    ref = re.findall(pattern_start_EngNumSpecial,i[2])
    newRef = ''.join(ref)
    # print(f'{len(newRef)} -> {newRef}')
    reference.append(newRef)

# print(reference)

#extract sender_name
sender_name = []
for i in list_data:
    sender_name.append(re.findall(pattern_only_Thai,i[4]))

# for name in sender_name:
#     print(name)
# print(len(sender_name))
# print(sender_name)


#extract sender_account_number
sender_account_number = []
for i in list_data:
    sender_account_number.append(re.findall(pattern_only_EngNum,i[4]))
# print(sender_account_number)


#extract receiptent_name
receiptent_name = []
index_biller = []
for i in list_data:
    # print(i)
    receiptent_name.append(re.findall(pattern_only_ThaiEngNum,i[6]))

receive_realname=[]
receive_accountNumber = []
for j in receiptent_name:
    try:
        index_biller.append(j.index('biller'))
    except:
        index_biller.append(-1)

    if index_biller[-1] == -1:
        receive_realname.append(j[:-1])
        receive_accountNumber.append(j[-1])
receiver_name=[]
before_receiver_name=[]
shop_name=[]
receiptentShop_name=[]
biller_id=[]
for index,x in enumerate(receiptent_name):
    if index_biller[index] != -1:
        biller_id.append(x[index_biller[index]+2:index_biller[index]+3])
        before_biller = x[:index_biller[index]]
        print(before_biller)
        if 'ชื่อบัญชี' in before_biller:
            receiver_name.append(before_biller[before_biller.index('ชื่อบัญชี'):])
            before_receiver_name.append(before_biller[:before_biller.index('ชื่อบัญชี')])
            #ชื่อก่อนบัญชี เป็น ชื่อร้าน 
            #ถ้าเป้นชื่อร้าน เราจะเรียกชื่อ บัญชี คือ บัญชี2
            shop_name.append(before_biller[:before_biller.index('ชื่อบัญชี')])
            receiptentShop_name.append(before_biller[before_biller.index('ชื่อบัญชี'):])
            
        else:
            before_biller.append(x[:index_biller[index]])

print(index_biller)
print(before_biller)
print('receiver - ------------')
print(receiver_name)

print('before -------------')
print(before_receiver_name)


print('receive_realname -------------')
print(receive_realname)

print('shop_name -------------')
print(shop_name)
print('receiptentShop_name -------------')
print(receiptentShop_name)
print(receive_accountNumber)
print(biller_id)
#extract ชื่อบัญชี
# for j in receiptent_name:
#     try:
#         index_biller.append(j.index('ชื่อบัญชี'))
#     except:
#         index_biller.append(-1)

# for name in receiptent_name:
#     print(name,'\n')

# print(receiptent_name)