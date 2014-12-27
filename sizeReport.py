#!/usr/bin/env python

import sys
import os
from PIL import Image

small = 100

if len(sys.argv) < 2:
    print "specify image path as parameter"
    sys.exit(1)
else:
    imagepath = sys.argv[1]

minh = 99999
maxh = 0
minw = 99999
maxw = 0
minpix = 99999**2
maxpix = 0
c = 0

print "doing the job"
for name in os.listdir(imagepath):  
    if name.rpartition('.')[2] in ('jpg', 'jpeg'):
        img = Image.open(os.path.join(imagepath, name))
        width, height = img.size
        if width < small or height < small:
            print "  small file: %s" % name
        mpix = width * height
        minh = min(minh, height)
        maxh = max(maxh, height)
        minw = min(minw, width)
        maxw = max(maxw, width)
        minpix = min(minpix, mpix)
        maxpix = max(maxpix, mpix)
        c += 1
        if c % 1000 == 0:
            print "%s: minW, maxW, minH, maxH, minMPix, maxMPix = %s, %s, %s, %s, %s, %s" % (c, minw, maxw, minh, maxh, minpix, maxpix)

print "minW, maxW, minH, maxH, minMPix, maxMPix = %s, %s, %s, %s, %s, %s" % (minw, maxw, minh, maxh, minpix, maxpix)
