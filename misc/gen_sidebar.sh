#!/bin/sh

MASK_IMAGE='mask_orig.png'
DESTINATION=$HOME/src/npca/data

cd $HOME/src/tmp

for arg in `ls sidebar*.png`; do convert $arg $MASK_IMAGE -composite $DESTINATION/${arg}; done
