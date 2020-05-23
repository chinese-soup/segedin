#!/bin/bash
# cd /var/www/segedin/
wget "http://www.umansfelda.cz/admin/pictures/0000000006.jpg" -O umansfelda.jpg
tesseract -l ces umansfelda.jpg mansfeld_ocr2
mv mansfeld_ocr2.txt mansfeld_ocr.txt