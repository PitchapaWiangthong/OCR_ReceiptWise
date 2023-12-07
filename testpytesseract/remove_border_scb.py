import cv2
import numpy as np

image = cv2.imread('testpytesseract\\dataset\\scb\\slip\\TXN_202308158P7Z2VHeg9iapyZjh.jpg')
highlight = image.copy()
original = image.copy()

def crop_border(contours,image):
    cntsSortedbyY = sorted(contours, key=lambda y:cv2.contourArea(y))
    cnt1 , cnt2 = cntsSortedbyY[-1] , cntsSortedbyY[-2]
    x, y1, w, h1 = cv2.boundingRect(cnt1)

    x, y2, w, h2 = cv2.boundingRect(cnt2)

    if y1 < y2:
        y_top = y1 + h1
        # y_btm = y2
    else:
        y_top = y2 + h2
        # y_btm = y1
    
    y_rect = []
    cntsSortedbyX = sorted(contours, key=lambda x:cv2.contourArea(x))
    for idx, cnt in enumerate(cntsSortedbyX):
        x, y, w, h = cv2.boundingRect(cnt)
        y_rect.append([abs(w-h),y])
    y_rect.sort()  
    crop = image[y_top:y_rect[0][1]] 
    return crop

# Convert image to grayscale, Otsu's threshold, and find contours
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)[1]
for i in range(150,255,5):
    thresh = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite(f'testpytesseract\\temp3\\test\\threshold\\thresh{i}.png', thresh)
print("thresh=",thresh)

# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
# print("rect_kernel =",rect_kernel)
# dilation = cv2.dilate(thresh, rect_kernel, iterations=2)
# print("dilation =",dilation)
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# print("contours =",contours)
# im2 =image.copy()
# crop = crop_border(contours,image.copy())

# crop = image[y:y+h, x:x+w]
# cv2.imwrite('testpytesseract\\temp3\\cropped.png', crop)


# for idx, cnt in enumerate(contours):
#     x, y, w, h = cv2.boundingRect(cnt)

#     # Cropping the text block for giving input to OCR
#     cropped = im2[y:y + h, x:x + w]
#     cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     # crop = image[y:y+h, x:x+w]
#     print(x,y,w,h)

# Save the cropped image to the output folder
# cv2.imwrite('testpytesseract\\temp3\\test\\bounding.png', im2)



















# Create black mask to extract desired objects
# mask = np.zeros(image.shape, dtype=np.uint8)

# Search for objects by filtering using contour area and aspect ratio
# for c in contours:
#     # Contour area
#     area = cv2.contourArea(c)
#     # Contour perimeter
#     peri = cv2.arcLength(c, True)
#     # Contour approximation
#     approx = cv2.approxPolyDP(c, 0.035 * peri, True)
#     (x, y, w, h) = cv2.boundingRect(approx)
#     aspect_ratio = w / float(h)
#     # Draw filled contour onto mask if passes filter
#     # These are arbitary values, may need to change depending on input image
#     if aspect_ratio <= 1.2 or area < 5000:
#         cv2.drawContours(highlight, [c], 0, (0,255,0), -1)
#         cv2.drawContours(mask, [c], 0, (255,255,255), -1)

# Convert 3-channel mask to grayscale then bitwise-and with original image for result
# mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# result = cv2.bitwise_and(original, original, mask=mask)

# Uncomment if you want background to be white instead of black
# result[mask==0] = (255,255,255)

# Display
# cv2.imshow('gray', gray)
# cv2.imshow('thresh', thresh)
# cv2.imshow('highlight', highlight)
# cv2.imshow('mask', mask)
# cv2.imshow('result', result)

# Save images
# cv2.imwrite('testpytesseract\\temp3\\test\\gray.png', gray)
# cv2.imwrite('testpytesseract\\temp3\\test\\thresh.png', thresh)
# cv2.imwrite('testpytesseract\\temp3\\test\\rect_kernel.png', rect_kernel)
# cv2.imwrite('testpytesseract\\temp3\\test\\dilation.png', dilation)
# cv2.imwrite('testpytesseract\\temp3\\contours.png', contours)

# cv2.imwrite('highlight.png', highlight)
# cv2.imwrite('mask.png', mask)
# cv2.imwrite('result.png', result)
cv2.waitKey(0)