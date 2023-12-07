# import datetime

# # Define a dictionary to map Thai month names to English month names
# thai_month_names = {
#     'ม.ค.': 'Jan',
#     'ก.พ.': 'Feb',
#     'มี.ค.': 'Mar',
#     'เม.ย.': 'Apr',
#     'พ.ค.': 'May',
#     'มิ.ย.': 'Jun',
#     'ก.ค.': 'Jul',
#     'ส.ค.': 'Aug',
#     'ก.ย.': 'Sep',
#     'ต.ค.': 'Oct',
#     'พ.ย.': 'Nov',
#     'ธ.ค.': 'Dec',
# }

# # Input string
# input_str = "02 ก.ย. 2566 09:03"

# # Split the input string into words
# words = input_str.split()

# # Extract day, month, year, and time components
# day = words[0]
# month = thai_month_names[words[1]]
# year = words[2]
# time = words[3]

# # Convert to a datetime object
# date_str = f"{day} {month} {year} {time}"
# date_object = datetime.datetime.strptime(date_str, "%d %b %Y %H:%M")

# # Format the datetime object in ISO 8601 format
# iso_8601_date = date_object.isoformat()

# print(iso_8601_date)

import datetime

# Define a dictionary to map Thai month names to English month names
thai_month_names = {
    'ม.ค.': 'Jan',
    'ก.พ.': 'Feb',
    'มี.ค.': 'Mar',
    'เม.ย.': 'Apr',
    'พ.ค.': 'May',
    'มิ.ย.': 'Jun',
    'ก.ค.': 'Jul',
    'ส.ค.': 'Aug',
    'ก.ย.': 'Sep',
    'ต.ค.': 'Oct',
    'พ.ย.': 'Nov',
    'ธ.ค.': 'Dec',
}

# Input date string
date_str = "07 ก.ค. 2566 12:26"

# Split the input date string into parts
parts = date_str.split()

# Extract day, month, year, and time components
day = parts[0]
month = thai_month_names[parts[1]]
# Convert Buddhist year to AD year by adding 543
year = int(parts[2]) - 543
time = parts[3]

# Create a datetime object
date_object = datetime.datetime(year, datetime.datetime.strptime(month, "%b").month, int(day), int(time.split(":")[0]), int(time.split(":")[1]))

# Add the timezone offset
date_with_timezone = date_object.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=7)))

# Format the datetime object in ISO 8601 format
iso_8601_date = date_with_timezone.isoformat()

print(iso_8601_date)
