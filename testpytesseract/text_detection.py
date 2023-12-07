# Import required packages
import cv2
import pytesseract
import os

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'
# Read image from which text needs to be extracted
img = cv2.imread("D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\dataset\\scb\\slip\\LINE_ALBUM_Scb_27.jpg")

# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size. 
# Kernel size increases or decreases the area 
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect 
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Creating a copy of the image
im2 = img.copy()

# Create a new directory to save cropped images
output_directory = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\temp2\\cropped_images"
os.makedirs(output_directory, exist_ok=True)

# A text file is created and flushed
file = open("D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\temp2\\ocr.txt", "w+", encoding="utf-8")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and saved to a new folder
# and passed on to pytesseract for extracting text from it
# Extracted text is then written into the text file
for idx, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)

    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]

    # Save the cropped image to the new folder
    output_path = os.path.join(output_directory, f"cropped_{idx}.png")
    cv2.imwrite(output_path, cropped)

    # Open the file in append mode
    file = open("D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\temp2\\ocr.txt", "a", encoding="utf-8")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped, lang='eng+tha', config='--psm 6')

    # Appending the text into the file
    file.write(text)
    file.write("\n")

    # Close the file
    file.close()

