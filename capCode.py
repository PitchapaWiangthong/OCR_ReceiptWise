# scb
# date(Date) 01 มิ.ย. 2566 08:11
# reference_Number = รหัสอ้างอิง: 20230601243qzddbcfh2xxund
# sender_name = นาย กฤษฎา สารวิทย์ 
# sender_account_number = xxx-xxx588-5
# receiptent_name = นาย อภิสิทธิ เนียมสูงเนิน 
# receiptent_account_number = xxx-xxx-9297
# amount = 35.00
# memo= [yo]

import re
results_ocr11=[
[[[438, 84], [804, 84], [804, 210], [438, 210]], 'oscb'],
[[[501, 381], [789, 381], [789, 449], [501, 449]], 'โอนเงินสำเร็จ'],
[[[449, 487], [839, 487], [839, 536], [449, 536]], '01 มิ.ย. 2566 20:44'],
[[[248, 550], [1039, 550], [1039, 613], [248, 613]], ' รหัสอ้างอิง: 202306018n8rr5xlh2bhoplvv'],
[[[67, 723], [147, 723], [147, 767], [67, 767]], ' จาก'],
[[[789, 715], [1232, 715], [1232, 857], [789, 857]], 'นาย กฤษฎา สารวิทย์  xxx-xxx588-5'],
[[[62, 912], [162, 912], [162, 966], [62, 966]], 'ไปยัง'],
[[[646, 914], [1228, 914], [1228, 1055], [646, 1055]], 'นางสาวฺณัฐธิดา วิเศษจิรโชค 1-5603-0008x-xx-x'],
[[[64, 1196], [254, 1196], [254, 1250], [64, 1250]], ' จำนวนเงิน'],
[[[1090, 1198], [1224, 1198], [1224, 1252], [1090, 1252]], '70.00'],
[[[61, 1398], [770, 1398], [770, 1549], [61, 1549]], 'ผู้รับเงินสามารกสแกนคิวอาร์โคัดนี้เพื่อ ตรวจสอบสถานะการโอนเงิน']

]
results_ocr12 = [[[[438, 84], [861, 84], [861, 210], [438, 210]], 'cscb.'], [[[501, 381], [789, 381], [789, 449], [501, 449]], 'โอนเงินสำเร็จ'], [[[450, 484], [838, 484], [838, 537], [450, 537]], '05 มิ.ย. 2566 21:30'], [[[262, 550], [1027, 550], [1027, 613], [262, 613]], ' รหัสอ้างอิง: 20230605968p83bjgaufutzk/'], [[[67, 723], [147, 723], [147, 767], [67, 767]], ' จาก'], [[[790, 718], [1230, 718], [1230, 857], [790, 857]], 'นาย กฤษฎา สารวิทย์  xxx-xxx588-5'], [[[62, 912], [162, 912], [162, 966], [62, 966]], 'ไปยัง'], [[[867, 917], [1225, 917], [1225, 1053], [867, 1053]], 'นาย วัชริศเชยชม  xxx-xxx-3528'], [[[64, 1196], [254, 1196], [254, 1250], [64, 1250]], ' จำนวนเงิน'], [[[1060, 1198], [1224, 1198], [1224, 1252], [1060, 1252]], '315.00'], [[[61, 1398], [770, 1398], [770, 1549], [61, 1549]], 'ผู้รับเงินสามารกสแกนคิวอาร์โคัดนี้เพื่อ ตรวจสอบสถานะการโอนเงิน']]
print(len(results_ocr11))
print(results_ocr11[1][1])
dataocr11 = []  # Initialize an empty list to store the values in data[i][1]

for item in results_ocr11:
    dataocr11.append(item[1])
stringlist_result = ''.join(dataocr11) 

# print(stringlist_result)
#date = 01 มิ.ย. 2566 08:15
date_pattern_brute = r'(\d{2}\s(?:ม\.ค\.|มี.ค\.|เม.ย\.|พ.ค\.|มิ.ย\.|ก.ค\.|ส.ค\.|ก.ย\.|ต.ค\.|พ.ย\.|ธ.ค\.)\s\d{4}\s\d{2}:\d{2})'
date_pattern_intermedate=r'(\d{2}\s(?:[ก-๛]\.[ก-๛]\.|[ก-๛][ก-๛]\.[ก-๛]\.)\s\d{4}\s\d{2}:\d{2})'
#text เติมเงินสำเร็จ 01 มิ.ย. 2566 08:15'],Here are some dates: 01 ม.ด. 2566 08:15, 05 ม.อ. 2566 21:30, and 18 ม.ค. 2566 13:59."
#will return  01 มิ.ย. 2566 08:15  01 ม.ด. 2566 08:15  05 ม.อ. 2566 21:30  18 ม.ค. 2566 13:59
match_date= re.findall(date_pattern_intermedate, stringlist_result)

print(match_date)
date= re.findall(date_pattern_intermedate, stringlist_result)

# reference_Number = รหัสอ้างอิง: 20230601243qzddbcfh2xxund
refference_pattern = r'รหัสอ้างอิง:\s*([0-9A-Za-z]*)'
matchreference = re.search(refference_pattern, stringlist_result)
if matchreference:
    match_reference = matchreference.group(1)

# sender_name = นาย กฤษฎา สารวิทย์ 
print('===========')
print(results_ocr11[5][1])
sender_namepattern=r'(นาย|นาง|น.ส.|u.ส.)[ก-๛ ]+'
res_sender_name=re.search(sender_namepattern, results_ocr11[5][1])
match_sender_name=res_sender_name.group()


# sender_account_number xxx-xxx-0502
sender_account_number = results_ocr11[5][1]
# print(res_sender_name.end())
# print(sender_account_number[20:])
sender_account_number = sender_account_number[res_sender_name.end():]


# receiptent_name = นาย อภิสิทธิ เนียมสูงเนิน 
res_receiptent_name=re.search(sender_namepattern, results_ocr11[7][1])
match_receiptent_name=res_receiptent_name.group()
print(res_receiptent_name)
print(match_receiptent_name)
# receiptent_account_number = xxx-xxx-9297
receiptent_account_number = results_ocr11[7][1]
receiptent_account_number = receiptent_account_number[res_receiptent_name.end():]
print(receiptent_account_number)


# amount = 35.00
amount = results_ocr11[9][1]


# memo= [yo]
print('********************************')
print("date:",match_date)
print("reference:",match_reference)
print("sender_name:",match_sender_name)
print("sender_account_number:",sender_account_number)
print("receiptent_name:",match_receiptent_name)
print("receiptent_account_number:",receiptent_account_number)
""" ถ้าเกิดมี shop ให้เพิ่มตัวแปร 
ชื่อบัญชี                   ชื่อบัญชี: อารีย์ รุ่งสง่า
ชื่อผู้รับก็จะเป็นร้านค้า         scb มณี sh0p ผัดไท ทอดหอย ป้าพัช
biilerID = เลขที่บัญชี      biller ld 010753600010286

'scb มณี sh0p ผัดไท ทอดหอย ป้าพัช} ชื่อบัญชี: อารีย์ รุ่งสง่า biller ld 010753600010286  รหัสร้านค้า : 014000002798908  รหัส อ้างอิงร้านค้า  scb เลขที่อ้างอิง 3 : 0000000000379147'] """