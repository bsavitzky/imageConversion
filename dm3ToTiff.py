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



# This function is based on Lena's MATLAB script dbl216.m
# Converts a floating point image to 16 bit uint16 format.
# Note that this should work to convert np.arrays of any dtype to uint16. 
# The image (matrix) is offset and rescaled to fit in 8 bits.

# I'm not totally clear on why this function is necessary - we convert the np.array to
# uint16 when we read it in, and it shouldn't need scaling...but apparently we do.  Some files
# seem to work fine without the scaling; others don't convert correctly without it (i.e. just look black).

def rescale(A):
    """Input: np.array A, dtype=floats.  Output: np.array with dtype=uint16, and values offset and rescaled
    NOTE: input must be an np.array!"""
    
    Amin = A[np.unravel_index(np.argmin(A),A.shape)]    #Finds min/max values in A
    Amax = A[np.unravel_index(np.argmax(A),A.shape)]

    B = np.zeros(A.shape)
#    B = np.zeros(A.shape, dtype='uint16')
    
    for i in range (0, A.shape[0]):
        for j in range (0, A.shape[1]):
            B[(i,j)] = np.uint16(round( (A[(i,j)] - Amin)*65535 / (Amax - Amin) ))
    
    return B



# Reads the .dm3 file, and writes it to a .tif

# TODO - Deal with rescaling.  Right now it doesn't scale properly, and rescaling is a pain because there are some data type
# issues.  Do dm3 files always store 32-bit data, or does it depend??  I think it varies...see the print call in the function below,
# giving the datatype as a number indexed in the DM3lib...

def dm3ToTiff(filename, newpath=getcwd()):

    dm3f = dm3.DM3(filename+".dm3", debug=0)
    A = dm3f.imagedata


    # get some useful tag data and print
    print "datatype:", dm3f.tags["root.ImageList.1.ImageData.DataType"]

#    A = rescale(A)
    
#    im = Image.fromarray(A, mode="I;16")     # "I;16" is PIL's 16 bit unsigned int mode - do we need this for dm3 files?
    im = Image.fromarray(A)
    im.save(newpath+"/"+filename+".tif", format="TIFF")
    
    return
    

parser = argparse.ArgumentParser(description="Converts .bin image files to .tiff format.")

parser.add_argument("files", nargs="*", help="File names you want converted!")
parser.add_argument("-a","--all", help="Converts all .bin files in your current directory, and puts them in a new directory named /Tiff.", action="store_true")
args = parser.parse_args()


# Converts all files in the cwd if -a (--all) option was specified:

if args.all:

    path = getcwd()
    mkdir(path+"/TiffsFromDm3Files")
    newDir = path+"/TiffsFromDm3Files"
    for f in listdir(path):
        if f.endswith(".dm3"):
            print "Converting", f,"from .dm3 to .tif"
            dm3ToTiff(f.replace(".dm3",""), newpath=newDir)


# Converts files listed as arguments:

else:
    for f in args.files:
        if f.endswith(".dm3"):
            f=f.rstrip(".dm3")
        print "Converting",f,"from .dm3 to .tif"
        dm3ToTiff(f)


        