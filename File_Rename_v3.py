from __future__ import print_function
import os, re, shutil


########
########Step 1: establish the shows and directories to be used
########

##############
############## 1.A Get the show list, add new show if needed
##############


print('Are you importing shows from this list?')
print()

#get showlist from txt file
showlistDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/showlist.txt')
showlistStr = showlistDoc.read()
showlist = showlistStr.split(', ') 
showlistDoc.close()

print(*showlist, sep='\n')
print('[Y/N]')
showInListYN = input()

#Check that they gave a valid Y or N
inputCheck = 0

if showInListYN.lower() == 'y':
    inputCheck = 1
elif showInListYN.lower() == 'n':
    inputCheck =1

while inputCheck == 0: 
    print('Please use Y or N to indicate if the shows you are renaming are in the above list?')
    showInListYN = input()
    if showInListYN.lower() == 'y':
        inputCheck = 1
    elif showInListYN.lower() == 'n':
        inputCheck =1

showInListYN = showInListYN.lower()

#If the show isn't included in the list, add it
if showInListYN == 'n':
    print('Please submit the name of the show')
    nameInput = input()
    print('Thank you!')

    nameInput = nameInput.title()
    print(nameInput)
        
    if nameInput not in showlist:
        showlist.append(nameInput)
        showlist.sort()
        print(showlist)              
    
        #Save the new Show list document
        writeshowlist = ", ".join(showlist)
        print(writeshowlist)
        showlistDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/showlist.txt', 'w')
        showlistDoc.write(writeshowlist)
        showlistDoc.close()






##############
############## 1.B Select Source Directory
##############

inPathDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/inputDirPath.txt')
inPathStr = inPathDoc.read()
inPathDoc.close()


if inPathStr == '':
    print('Please input the current path to your files:')
    inPathStr = input()
else:
    print('Last time you got your files from: ')
    print(inPathStr)
    print('Would you like to use the same source? [Y/N]')
    newpathcheck = input()
    newpathcheck = newpathcheck.lower()

    if newpathcheck == 'n':
        print("Please submit the new source (Note: file will search all subfolders contained within, so you don't have to rearrange the files.")
        inPathStr = input()
        print('Great!')

if inPathStr[-1] != '/':
    inPathStr = ''.join((inPathStr,'/'))

inPathDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/inputdirpath.txt', 'w')
inPathDoc.write(inPathStr)
inPathDoc.close()






##############
############## 1.C Select Output Directory
##############


outPathDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/outputDirPath.txt')
outPathStr = outPathDoc.read()
outPathDoc.close()


if outPathStr == '':
    print('Please input the the path to where you would like your files to end up:')
    outPathStr = input()
else:
    print('Last time you put your files in here: ')
    print(outPathStr)
    print('Would you like to use the same location? [Y/N]')
    newpathcheck = input()
    newpathcheck = newpathcheck.lower()

    if newpathcheck == 'n':
        print('Please submit the new output folder') 
        outPathStr = input()
        print('Great!')

if outPathStr[-1] != '/':
    outPathStr = ''.join((outPathStr,'/'))

outPathDoc = open('/Users/JohnAdam/Documents/Automate_the_Boring_Things_Using_Python/Programs/FileRename/outputdirpath.txt', 'w')
outPathDoc.write(outPathStr)
outPathDoc.close()











#os.chdir(directoryInput + '/')





########
########Step 2: Find shows, rename them and move them
######## 


for folderName, subFolders, fileNames in os.walk(inPathStr):

    for fileName in fileNames:

        if fileName.endswith('.mp4') or fileName.endswith('.avi') or fileName.endswith('.mpeg') or fileName.endswith('.mkv'):

            #Check file name against the list of shows in the dictionary
            for show in showlist:
                
                titleLength = show.count(' ')
                #Extract and clean filename
                nameRegex = re.compile(r'[a-zA-Z ]+')
                extractedName = nameRegex.findall(fileName)                
                extractedName = extractedName[0:titleLength+1]
                name = ""
               
                ##Clean viaTurning name list into a string
                for i in extractedName:
                    name = name + i + ' '
                                
                name = name.strip()
                name = name.title()

                if name.lower() == show.lower():

                    #Extract and clean file type
                    fileTypeRegex = re.compile(r'(\.\w{3,}$)')
                    extractedFileType = fileTypeRegex.findall(fileName)

                    extractedFileTypeStr = extractedFileType[0]


                    #Extract and clean episode and season #s
                    episodeRegex = re.compile(r'\w\d\d\w\d\d')
                    episodeRegex2 = re.compile(r'\D\d\d\d\D')
                    
                    ##Account for different types of
                    if not episodeRegex.findall(fileName):
                        extractedEpisode = episodeRegex2.findall(fileName)
                    else:
                        extractedEpisode = episodeRegex.findall(fileName)

                    season = ""
                    episode = ""

                    ##Clean episode ID
                    extractedEpisodeStr = extractedEpisode[0]
                    extractedEpisodeStr = extractedEpisodeStr.strip('.')
                    if len(extractedEpisodeStr) == 3:
                        season = extractedEpisodeStr[0]
                        episode = extractedEpisodeStr[1:]
                        extractedEpisodeStr = 'S0' + season + 'E' + episode
                    elif len(extractedEpisodeStr) == 6:
                        season = extractedEpisodeStr[2]

                    
                    
                    #Use extracted information to create the new file title
                    newFile = name + " " + extractedEpisodeStr + extractedFileTypeStr
                    newFolder = name + " - Season " + season

                    #Check if target folder exists                
                    oldPath = folderName + '/'
                    newPath = outPathStr + '/' + show + '/' + show + ' - Season ' + season + '/'

                    if not os.path.exists(newPath):
                        os.makedirs(newPath)

                    shutil.move(oldPath + fileName, newPath + newFile)

                    print('Clean and move from: ' + oldPath + fileName)
                    print('To :' + newPath + newFile + '\n\n') 




print('Done!')

#######
##Work to be done
#Bug 1: Does not work on file names that don't use . for separation (e.g. Lucha Underground)
#Task 1: Delete folders when empty 
#Task 2: Figure out how to detect the show name from the filename
