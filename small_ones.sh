#!/bin/bash
#
# create small versions of images and try to keep metadata
# by first extracting via exiv2, convert, re-insert metadata


which exiv2 > /dev/null
if [ $? -ne 0 ];
then
 echo "exiv2 not found."
 exit 1
fi

which convert > /dev/null
if [ $? -ne 0 ];
then
 echo "exiv2 not found."
 exit 1
fi

if [ $# -eq 0 ]
then
 echo "parameter missing -- specify directory to process"
 exit 1
fi

if [ -d $1 ]
then
 echo "processing directory $1"
else
 echo "is not a directory: $1"
 exit 1
fi

cd $1
mkdir small_ones

for FILE in *.jpg
do
 E=${FILE%.*}.exv
 exiv2 ex $FILE
 convert $FILE -resize 1024x1024\> small_ones/$FILE
 mv $E small_ones/
 exiv2 in small_ones/$FILE
 rm small_ones/$E
done
