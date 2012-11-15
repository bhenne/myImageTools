#!/usr/bin/env python
#
# iterate over a file or over a directory recursively
# read all metadata fields and count the occurence
# of the metadata entries across all files

import pyexiv2
import sys
from os import path, walk

__author__ = "B. Henne"
__contact__ = "henne@dcsec.uni-hannover.de"
__copyright__ = "(c) 2012, B. Henne"
__license__ = "GPLv3"

md = {}
n = 0
infoeach = 100
fileeach = 1000
statsfile = "/tmp/md_count_stats.txt"

def check(dirpath, filename):
    global md, n
    if dirpath is not None:
        filename = '%s/%s' % (dirpath, filename)
    try:
        m = pyexiv2.ImageMetadata(filename)
        m.read()
    except:
        return
    n+=1
    if n % infoeach == 0:
        print n, filename
    if n % fileeach == 0:
        writestats()
    for l in (m.exif_keys, m.iptc_keys, m.xmp_keys):
        for k in l:
            # have to look if tag may be empty?
            if k in md:
                md[k] = md[k]+1
            else:
                md[k] = 1

def stats():
    for k in sorted(md):
        print "%s: %s" % (k, md[k])
    writestats()

def writestats():
    f = open(statsfile, "wt")
    f.write("%s\n" % n)
    for k in sorted(md):
        f.write("%s: %s\n" % (k, md[k]))
    f.close()

def main():
    if len(sys.argv) > 1:
        if path.isdir(sys.argv[1]):
            for dirpath, dirnames, filenames in walk(sys.argv[1]):
                for filename in filenames:
                    check(dirpath, filename)
            stats()
        elif path.isfile(sys.argv[1]):
            check(None, sys.argv[1])
            stats()
        else:
            print 'Usage %s file|directory' % sys.argv[0]
    else:
        print 'Usage %s file|directory' % sys.argv[0]

if __name__ == '__main__':
    main()
