import cv2
import os
import numpy as np

def crop_border(contours, image):
    cntsSortedbyY = sorted(contours, key=lambda y: cv2.contourArea(y))
    cnt1, cnt2 = cntsSortedbyY[-1], cntsSortedbyY[-2]
    x, y1, w, h1 = cv2.boundingRect(cnt1)
    x, y2, w, h2 = cv2.boundingRect(cnt2)

    if y1 < y2:
        y_top = y1 + h1
    else:
        y_top = y2 + h2

    y_rect = []
    cntsSortedbyX = sorted(contours, key=lambda x: cv2.contourArea(x))
    for idx, cnt in enumerate(cntsSortedbyX):
        x, y, w, h = cv2.boundingRect(cnt)
        y_rect.append([abs(w-h), y])
    y_rect.sort()  
    crop = image[y_top:y_rect[0][1]] 
    return crop

def bounding_image(contours, image):
    for idx, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        # Cropping the text block for giving input to OCR
        cropped = image[y:y + h, x:x + w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return image  # Returning the image with bounding boxes

# Specify input and output folders
input_folder = 'testpytesseract\\dataset\\scb\\slip'
output_folder_cropped = 'testpytesseract\\temp3\\cropped'
output_folder_bounded = 'testpytesseract\\temp3\\bounded'
output_folder_dilation = 'testpytesseract\\temp3\\dilation'


# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.JPG')):  # Filter images based on file extensions
        # Read the image
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Unable to read image: {image_path}")
            continue

        # Your existing code for processing and cropping
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
        dilation = cv2.dilate(thresh, rect_kernel, iterations=2)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # Process and save dilation image
        output_path_dilation = os.path.join(output_folder_dilation, f'dilation_{filename}')
        cv2.imwrite(output_path_dilation, dilation)
        print(f"Dilation and saved: {output_path_dilation}")


        # Process and save bounded image
        bounded = bounding_image(contours, image.copy())
        output_path_bounded = os.path.join(output_folder_bounded, f'bounded_{filename}')
        cv2.imwrite(output_path_bounded, bounded)
        print(f"Bounded and saved: {output_path_bounded}")

        # Process and save cropped image
        crop = crop_border(contours, image.copy())
        output_path_cropped = os.path.join(output_folder_cropped, f'cropped_{filename}')
        cv2.imwrite(output_path_cropped, crop)
        print(f"Cropped and saved: {output_path_cropped}")

