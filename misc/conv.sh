#!/bin/sh

root=`pwd`

python ./a ${root}

mkdir alpha
for arg in `ls *.jpg`; do convert $arg -alpha On -channel A -fx "(r<0.15&&b<0.15&&g<0.15)?0:1" ${root}/alpha/${arg}.alpha.png; done
cd alpha

mkdir resize
for arg in `ls *.png`; do convert -resize 32x32 $arg ${root}/alpha/resize/${arg}.resize.png; done
cd resize

convert +append *.png out.png
