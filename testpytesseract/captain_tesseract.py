import PIL
from PIL import Image,ImageDraw,ImageFont
import cv2
import os
import pytesseract
# read image and convert to RGB
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

font_size=17
font = ImageFont.truetype(r"testpytesseract\THSarabunNew.ttf",font_size)
# w,h = image.size
images=[]
ocr_result = []
filename_list=[]
# create image and ocr txt
directory_folder_source=r'testpytesseract\dataset\kbank\slip_test'
for filename in os.listdir(directory_folder_source):
    if os.path.isfile(os.path.join(directory_folder_source, filename)):
        image= cv2.imread(os.path.join(directory_folder_source, filename))
        # image = image[170:]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #binarize
        thresh=cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)[1]
        cv2.imwrite(f"testpytesseract\captain_iterate_asset\\threshold\kbank_thresh150_{filename}.png",thresh)

        #image to string
        ocr_text = pytesseract.image_to_string(image, lang="tha+eng")
        
        #resize image to store
        base_width=300
        wpercent=(base_width/image.shape[1])
        hsize = int((image.shape[0]*float(wpercent)))
        dim = (base_width, hsize)
        
        # resize image
        image= cv2.resize(thresh, dim, interpolation = cv2.INTER_AREA)
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        
        image = Image.fromarray(image) 
        filename_list.append(filename)
        images.append(image)
        ocr_result.append(ocr_text)

# Write to filename.txt
with open('filename.txt', 'w') as f:
    for filename in filename_list:
        f.write(f"{filename}\n")

# Write to images.txt
with open('images.txt', 'w') as f:
    for img in images:
        f.write(f"{img}\n")

# Write to ocr.txt
with open('ocr.txt', 'w', encoding='utf-8') as f:
    for ocr_text in ocr_result:
        f.write(f"{ocr_text}**********************\n")
        f.write(f"{ocr_text}\n")
        
# create a contact sheet from images
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (int(first_image.width*2.6),first_image.height*(len(images))+(font_size)*len(images)))
x=0
y=0
draw = ImageDraw.Draw(contact_sheet)
i=0
for img in images:
    # Lets paste the current image into the contact sheet
    draw.text((x,y), text=f'{filename_list[i]}', fill='white', font=font, align="left")
    y+=font_size
    contact_sheet.paste(img, (x, y) )

    draw.text((x+base_width+font_size,y), text=ocr_result[i],fill='white', font=font, align="left")
    y=y+first_image.height+200
    x=0

    i+=1

# resize and display the contact sheet

contact_sheet.save('testpytesseract\\kbank_thresh150.png')
contact_sheet.show() 