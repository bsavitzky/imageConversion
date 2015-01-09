#! /usr/bin/env python

import numpy as np
from struct import unpack
import Image
from os import getcwd, mkdir, listdir
import argparse

import DM3lib as dm3


# This script converts .dm3 image files to .tif files.
# Syntax for use is:
#       python dm3ToTiff.py file1 file2 file3 ...

# If the -a or --all option is specified, all .bin files in the current directory are
# converted, and saved in a new folder, /Tiffs


# Written by Ben Savitzky 2014-01-21

# The core of this code is the pyDM3reader package, and specifically it's DM3lib library,
# written by Pierre-Ivan Raynal, which was in turn based on the DM3_Reader plug-in for imageJ,
# written by Greg Jefferis.



# Reads the .dm3 file, and writes it to a .png - mostly from Pierre-Ivan Raynal's DM3 reader demo.py


def dm3ToPNG(filename, newpath=getcwd()):

    dm3f = dm3.DM3(filename+".dm3", debug=0)
    A = dm3f.imagedata
    cuts = dm3f.cuts

    A_norm = A.copy()
    
    if cuts[0] != cuts[1]:
        A_norm[ (A <= min(cuts)) ] = float(min(cuts))
        A_norm[ (A >= max(cuts)) ] = float(max(cuts))
    # -- normalize
    A_norm = (A_norm - np.min(A_norm)) / (np.max(A_norm) - np.min(A_norm))
    # -- scale to 0--255, convert to (8-bit) integer
    A_norm = np.uint8(np.round( A_norm * 255 ))

    # - save as PNG and JPG
    im = Image.fromarray(A_norm)
    im.save(newpath+"/"+filename+".png", format="PNG")

    
    return
    

parser = argparse.ArgumentParser(description="Converts .dm3 image files to .png format.")

parser.add_argument("files", nargs="*", help="File names you want converted!")
parser.add_argument("-a","--all", help="Converts all .bin files in your current directory, and puts them in a new directory named /Tiff.", action="store_true")
args = parser.parse_args()


# Converts all files in the cwd if -a (--all) option was specified:

if args.all:

    path = getcwd()
    mkdir(path+"/PNGsFromDm3Files")
    newDir = path+"/PNGsFromDm3Files"
    for f in listdir(path):
        if f.endswith(".dm3"):
            print "Converting", f,"from .dm3 to .png"
            dm3ToPNG(f.replace(".dm3",""), newpath=newDir)


# Converts files listed as arguments:

else:
    for f in args.files:
        if f.endswith(".dm3"):
            f=f.replace(".dm3","")
        print "Converting",f,"from .dm3 to .png"
        dm3ToPNG(f)


        