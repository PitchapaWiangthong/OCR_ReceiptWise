import cv2
import os
import numpy as np

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def remove_borders(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return crop

def preprocess_and_crop(input_folder, output_folder_prepro, output_folder_crop):

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg','.JPG')):
            # Construct the full path to the input image
            input_image_path = os.path.join(input_folder, filename)

            # Read the input image
            img = cv2.imread(input_image_path)

            # Apply preprocessing steps
            gray_image = grayscale(img)
            _, im_bw = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
            no_noise = noise_removal(im_bw)
            no_borders = remove_borders(no_noise)

            # Specify the output filename for the preprocessed image
            preprocessed_filename = os.path.join(output_folder_prepro, f"preprocessed_{filename}")

            # Save the preprocessed image
            cv2.imwrite(preprocessed_filename, no_borders)

            # Specify the output filename for the cropped image
            cropped_filename = os.path.join(output_folder_crop, f"cropped_{filename}")

            # Crop the preprocessed image
            # amount = 210:280,0:622
            # date = 350:385, 160:350
            y_start, y_end, x_start, x_end = 260,330, 315,600 
            cropped_img = no_borders[y_start:y_end, x_start:x_end]

            # Save the cropped image
            cv2.imwrite(cropped_filename, cropped_img)

            print(f"Cropped and preprocessed image saved to {cropped_filename}")

# Specify input folder and output folder
input_folder = "testpytesseract\\dataset\\aomsin\\slip"
output_folder_prepro = "testpytesseract\\dataset\\aomsin\\preprocessed\\"
output_folder_crop = "testpytesseract\\dataset\\aomsin\\section\\crop\\date\\"
# Perform preprocessing on all images in the input folder
preprocess_and_crop(input_folder, output_folder_prepro, output_folder_crop)
