#!/usr/bin/env python
#
# check if file(s) are images or not, find broken downloads and so on

from PIL import Image
#import pyexiv2
import sys
from os import path, walk
#from mimetypes import guess_type
from magic import magic # https://github.com/ahupp/python-magic

__author__ = "B. Henne"
__contact__ = "henne@dcsec.uni-hannover.de"
__copyright__ = "(c) 2012, B. Henne"
__license__ = "GPLv3"

mime = magic.Magic(mime=True)

def check(filename, dirpath=None):
    if dirpath is not None:
        filename = '%s/%s' % (dirpath, filename)
    #t = guess_type(filename)[0] # used only file extension
    t = mime.from_file(filename)
    if t is not None and t.startswith('image'):
	try:
            img = Image.open(filename)
	    #m = pyexiv2.ImageMetadata(filename)
	    #m.read()
	except:
	    sys.stderr.write('Error at file %s (%s)\n' % (filename, t))
	    return
	    #raise
    else:
        if (len(sys.argv) > 2) and (sys.argv[2] == 'f'):
            sys.stderr.write('%s\n' % filename)
        else:
            sys.stderr.write('No image in %s (%s)\n' % (filename, t))

def main():
    if len(sys.argv) > 1:
         if path.isdir(sys.argv[1]):
	     for dirpath, dirnames, filenames in walk(sys.argv[1]):
                 for filename in filenames:
	             check(filename, dirpath)
         elif path.isfile(sys.argv[1]):
             check(sys.argv[1])
         else:
             print 'Usage %s file|directory [f]\n f  as optional second parameter switches to only output filenames' % sys.argv[0]
    else:
        print 'Usage %s file|directory [f]\n f  as optional second parameter switches to only output filenames' % sys.argv[0]

if __name__ == '__main__':
    main()
