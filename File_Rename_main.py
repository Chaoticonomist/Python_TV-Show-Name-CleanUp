from __future__ import print_function
import os, re, shutil

from File_Rename_v5 import *



SHOW_LIST_DOC = "/Users/JohnAdam/Documents/Coding/Python/Programs/FileRename/showlist.txt"
INPUT_DIRECTORY_DOCUMENT = "/Users/JohnAdam/Documents/Coding/Python/Programs/FileRename/inputDirPath.txt"
OUTPUT_DIRECTORY_DOCUMENT = "/Users/JohnAdam/Documents/Coding/Python/Programs/FileRename/outputDirPath.txt"
docPathstr = ''
showlist = ''


print ('Welcome to the file renamer! \n\n')

#Determine shows

def interface():
    print ("Here are the shows you've told us that you watch: \n")
    showShowList(SHOW_LIST_DOC)
    checkToAddShow(SHOW_LIST_DOC)
   
    chooseDirectory("source",INPUT_DIRECTORY_DOCUMENT)
    chooseDirectory("output",OUTPUT_DIRECTORY_DOCUMENT)

interface()
    
cleanAndMove(INPUT_DIRECTORY_DOCUMENT, OUTPUT_DIRECTORY_DOCUMENT, SHOW_LIST_DOC)    

print('\n Done!!!')

### More featuers to add
#Option to move or not move files
#Multiple options to choose from for input/output directories
