#!/bin/bash

# output_path=./
input_path=ocr_text/

for file in $input_path*
do
    ocr_text=$(python mapping.py "$file")
    echo "OCR from $file\n$ocr_text\n" >> ocr_all.txt

done