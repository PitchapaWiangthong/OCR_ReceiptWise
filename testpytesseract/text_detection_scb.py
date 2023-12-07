# Import required packages
import cv2
import pytesseract
import os

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# Specify the folder containing the images
input_folder = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\dataset\\scb\\slip"

# Create a new directory to save bounded images
output_folder = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\temp2\\bound_images"
os.makedirs(output_folder, exist_ok=True)

# A text file is created and flushed
output_txt_path = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\temp2\\ocr.txt"
file = open(output_txt_path, "w+", encoding="utf-8")
file.write("")
file.close()

# Loop through each image in the input folder
for image_file in os.listdir(input_folder):
    # Read image from the input folder
    image_path = os.path.join(input_folder, image_file)
    img = cv2.imread(image_path)

    # Preprocessing the image starts
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of the image
    im2 = img.copy()

    # Looping through the identified contours
    # Then rectangular part is cropped and saved to a new folder
    # and passed on to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    
    for idx, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the cropped image to the output folder
        output_path = os.path.join(output_folder, f"bounded_{image_file}")
        cv2.imwrite(output_path, im2)

        # Open the file in append mode
        file = open(output_txt_path, "a", encoding="utf-8")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped, lang='eng+tha', config='--psm 6')

        # Append the OCR text and image filename to the text file
        file.write(f"Image: {image_file}\n")
        file.write(f"Text: {text}\n")
        file.write("\n")

        # Close the file
        file.close()
