import PIL
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

images = []
ocr_result = []
filename_list = []

directory_folder_source = r'testpytesseract\dataset\krungthai\slip_test'
output_folder_ocr_text = r'testpytesseract\OCR\krungthai\ocr_text'

# Create the output folder if it doesn't exist
os.makedirs(output_folder_ocr_text, exist_ok=True)

for filename in os.listdir(directory_folder_source):
    if os.path.isfile(os.path.join(directory_folder_source, filename)):
        image = cv2.imread(os.path.join(directory_folder_source, filename))
        image = image[170:]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Binarize
        thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imwrite(f"testpytesseract\OCR\krungthai\\threshold_image\\krungthai_thresh200_{filename}.png", thresh)

        # Image to string
        ocr_text = pytesseract.image_to_string(image, lang="tha+eng")
        # Remove spaces from the OCR result
        new_res = "".join(['' if i == ' ' else i for i in ocr_text])

        # Append the OCR result to the list
        ocr_result.append(new_res)

        # Save OCR result to text file
        output_file_path = os.path.join(output_folder_ocr_text, f'ocr_result_{filename}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f"{new_res}")
            print(f"OCR result saved to: {output_file_path}")

with open('testpytesseract\OCR\krungthai\ocr.txt', 'w', encoding='utf-8') as file:
    for i, result in enumerate(ocr_result):
        file.write(f"OCR Result for Image {filename}:\n{result}\n{'-'*30}\n")
