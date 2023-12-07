import cv2
import os

image_path = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\dataset\\aomsin\\image\\IMG_2950.JPG"
img = cv2.imread(image_path)

# Specify the cropping region
y_start, y_end, x_start, x_end = 205, 280, 0, 622
crop_img = img[y_start:y_end, x_start:x_end]

# Get the dimensions of the original image
h, w, _ = img.shape
print('width:', w)
print('height:', h)

# Specify the output directory for the cropped images
output_folder = "D:\\homework\\D4-1\\OCR_ReceiptWise\\testpytesseract\\dataset\\aomsin\\section\\crop\\amount\\"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save the cropped image with a numbered filename
output_filename = os.path.join(output_folder, f"cropped_{len(os.listdir(output_folder)) + 1}.jpg")
cv2.imwrite(output_filename, crop_img)

print(f"Cropped image saved to {output_filename}")
