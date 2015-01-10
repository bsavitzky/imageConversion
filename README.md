These python scripts convert .bin or .dm3 image files to .PNG .tif file formats.

DM3 file conversion scripts are a thin wrapper Pierre-Ivan Raynal's python code, which is in turn based on Greg Jefferis's ImageJ DM3 reader.  See: https://github.com/jrminter/snippets/tree/master/pyDM3reader

Typical usage is:

python binToTiff.py [filename]
python binToTiff.py -a

The -a option converts all .bin files in the pwd, and places them all in a new directory called TiffFromBinFiles.  Similarly for converting from dm3's, to PNG's, etc.





