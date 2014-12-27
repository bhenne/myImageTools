#!/usr/bin/env python
#
# match image width/height ratio against those of its integrated previews
# try to find image with more (not cut) content in preview
# these could maybe show explicit/private content
# -- not 100% perfectly done, to be improved --

from PIL import Image
import pyexiv2
import sys
from os import path, walk
#from mimetypes import guess_type
from magic import magic # https://github.com/ahupp/python-magic

__author__ = "B. Henne"
__contact__ = "henne@dcsec.uni-hannover.de"
__copyright__ = "(c) 2012, B. Henne"
__license__ = "GPLv3"

ok = 0        # counter
deltaf = 0.10 # delta in float w/h ratio
deltap = 2    # delta in pixels

mime = magic.Magic(mime=True)

def match(dirpath, filename):
    global ok
    if dirpath is not None:
        filename = '%s/%s' % (dirpath, filename)
    #t = guess_type(filename)[0] # used only file extension
    t = mime.from_file(filename)
    if t is not None and t.startswith('image'):
	try:
            img = Image.open(filename)
	    w, h = img.size
	    landscape = (w > h)
	    r = float(w)/h
	    m = pyexiv2.ImageMetadata(filename)
	    m.read()
	except:
	    sys.stderr.write('Exception at file %s\n' % filename)
	    return
	    #raise
        if len(m.previews) > 0:
	    for p in m.previews:
		pw, ph = p.dimensions
		plandscape = (pw > ph)
		pr = float(pw)/ph

                ## RATIO CHECKS
		# both images are lanscape or not
		if landscape == plandscape:
		    # same size, using delta as ratio difference
		    if (abs(r - pr) <= deltaf):
		        ok += 1
		        continue
		# one image is landscape other is not
		else:
	            # same size, using delta as ratio difference
	            if (abs(r - 1.0/pr) <= deltaf):
		        ok += 1
		        continue

                ## SIZE CHECKS
		# both images are lanscape or not
		if landscape == plandscape:
	            wc = h/ph*pw # calculate image width by its height and the previews ratio
		    if (abs(w-wc) <= deltap):
		        ok += 1
		        continue
		# one image is landscape other is not
		else:
	            wc = h/pw*ph # calculate image width by its height and the previews ratio
		    if (abs(w-wc) <= deltap):
	                ok += 1
			continue

		if (len(sys.argv) > 2) and (sys.argv[2] == 'f'):
		    print filename
		else:
                   print filename, 'image(%s,%s) preview(%s,%s) ratio %s =! %s d=%s' % (w,h,pw,ph,r,pr,abs(r-pr))
    else:
        sys.stderr.write('Wrong file type of %s: %s\n' % (filename, t))

def main():
    if len(sys.argv) > 1:
         if path.isdir(sys.argv[1]):
	     for dirpath, dirnames, filenames in walk(sys.argv[1]):
                 for filename in filenames:
	             match(dirpath, filename)
         elif path.isfile(sys.argv[1]):
             match(None, sys.argv[1])
         else:
             print 'Usage %s file|directory [f]\n f  as optional second parameter switches to only output filenames' % sys.argv[0]
    else:
        print 'Usage %s file|directory [f]\n f  as optional second parameter switches to only output filenames' % sys.argv[0]
    print '%s files had matching previews' % ok

if __name__ == '__main__':
    main()
