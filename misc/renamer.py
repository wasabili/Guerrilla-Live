#!/usr/bin/env python

import sys
DIR = sys.argv[1]
import os
import re
filelist = os.listdir(DIR)
print filelist
for f in filelist:
    mm = re.match(r'Player(.+)\.jpg', f)
    num = mm.group(1)
    if int(num) < 10:
        b = '00'+num
    elif int(num) < 100:
        b = '0' +num
    else:
        b = num
    new = DIR+'/'+f
    old = DIR+'/Player'+b+'.jpg'
    os.rename(new, old)


