import os
from PIL import Image
import pytesseract

# Set Tesseract executable and data path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# Folder containing the images
folder_path = 'D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\dataset\\scb\\section\\crop\\date'

# List to store OCR results
ocr_array = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg','.JPG')):
        # Construct the full path to the image
        image_path = os.path.join(folder_path, filename)

        # Open the image using PIL
        img = Image.open(image_path)

        # Perform OCR on the image
        ocr_result = pytesseract.image_to_string(img, lang='tha', config='--psm 6')

        # Remove spaces from the OCR result
        new_res = "".join(['' if i == ' ' else i for i in ocr_result])

        # Append the OCR result to the list
        ocr_array.append(new_res)

        # Print the OCR result for the current image
        print(f"OCR Result for {filename}:\n{new_res}\n{'-'*30}")

# Save OCR results to a text file
output_file_path = 'testpytesseract\\output_ocr_crop\\ocr_scb_date_tha6.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    for i, result in enumerate(ocr_array):
        file.write(f"OCR Result for Image {filename}:\n{result}\n{'-'*30}\n")

print(f"OCR results saved to {output_file_path}")