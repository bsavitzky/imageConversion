#! /usr/bin/env python

import numpy as np
from struct import unpack
import Image
from os import getcwd, mkdir, listdir
import argparse


# This script converts .bin image files to .tif files.
# Syntax for use is:
#       python binToTiff.py file1 file2 file3 ...

# If the -a or --all option is specified, all .bin files in the current directory are
# converted, and saved in a new folder, /Tiffs


# Written by Ben Savitzky 2013-10-17
# With help from Xue Bai's and Lena Kourkoutis' code!



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

    B = np.zeros(A.shape, dtype='uint16')
    
    for i in range (0, A.shape[0]):
        for j in range (0, A.shape[1]):
            B[(i,j)] = np.uint16(round( (A[(i,j)] - Amin)*65535 / (Amax - Amin) ))
    
    return B


# This function is based on Lena's MATLAB script readbin.m
# Reads a .bin file into a [pix,pix] np.array.  Note that the header is 10 bytes,
# and the rest of the file should be just data, in uint16 format...

def readBin(filename):
    """Input: name of the file, and the image pixel size (assumes square image)
    Output: a np.array of size ([pix,pix]), dtype uint16, of the image data.
    
    Assumes data is uint16, and the header is 10 bytes."""

    f=open(filename,'rb')
    
    #Read the header, get dimensions
    
    data = f.read(2)   # Data type, not sure how it's coded...
    data = f.read(4)
    pixX = unpack("<i",data)[0]        #unpack, from struct module, reads binary strings.  
                                        #"i" = 4 bit int.  ">"=little endian.  [0] b/c output is a tuple
    data = f.read(4)
    pixY = unpack("<i",data)[0]
        
    A = np.zeros((pixX,pixY), dtype='uint16')
        
    #Write into an np.array
    for i in range (0,pixX):
        for j in range (0,pixY):
            data = f.read(2)
            if data == "":
                print "Error. Ran out of data, pix dimensions may be wrong."
                return None
            else:
                A[(i,j)]=unpack("<H",data)[0]   #unpack, from struct module, reads binary strings.  
                                                #"H" = uint16.  ">"=little endian.  [0] b/c output is a tuple
            
    f.close()
    return A


# Reads the .bin file, and writes it to a .tiff

def binToTiff(filename, newpath=getcwd()):
    
    A = readBin(filename+".bin")
    A = rescale(A)
    
    im = Image.fromarray(A, mode="I;16")     # "I;16" is PIL's 16 bit unsigned int mode
    im.save(newpath+"/"+filename+".tif", format="TIFF")
    
    return
    

parser = argparse.ArgumentParser(description="Converts .bin image files to .tiff format.")

parser.add_argument("files", nargs="*", help="File names you want converted!")
parser.add_argument("-a","--all", help="Converts all .bin files in your current directory, and puts them in a new directory named /Tiff.", action="store_true")
args = parser.parse_args()


# Converts all files in the cwd if -a (--all) option was specified:

if args.all:

    path = getcwd()
    mkdir(path+"/Tiffs")
    newDir = path+"/Tiffs"
    for f in listdir(path):
        if f.endswith(".bin"):
            print "Converting", f,"from .bin to .tif"
            binToTiff(f.replace(".bin",""), newpath=newDir)


# Converts files listed as arguments:

else:
    for f in args.files:
        if f.endswith(".bin"):
            f=f.replace(".bin","")
        print "Converting",f,"from .bin to .tif"
        binToTiff(f)


        