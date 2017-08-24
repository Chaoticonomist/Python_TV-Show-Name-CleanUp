from __future__ import print_function
import os, re, shutil

##Functions for TV Show file renaming program

##Program Guide
###Step 1: user interface
#### 1.A Make sure all relevant shows are included in the search
#### 1.B Select Directories
###Step 2: Find shows, rename them and move them


#makes sure input is Y or N
def getReply():
    userResponse = input()
    while userResponse.lower() != 'y' and userResponse.lower() !='n':  
        print('\n Please use Y or N with quotation marks to indicate your response.')
        userResponse = input()
    return userResponse.lower()
    
########
########Step 1: establish the shows and directories to be used
########

##############
############## 1.A Get the show list, add new show if needed
##############


# see if you want to add any shows to the list    
def checkToAddShow(showlistFile):    
    print('\nDo you want to add any shows to the list? [Y/N]')
    reply = getReply()
    while reply != 'n':
        addShow(showlistFile)
        print('\nDo you want to add any more shows to the list? [Y/N]')
        reply = getReply()        
            
#add shows to the list   
def addShow(showListFile):    
    print('\nPlease submit the name of the show in quotation marks')
    addShowName = input()
    addToShowlist(addShowName, showListFile)
    print('\nThank you! ' + addShowName + ' is now in the list!')  
    

        
###Working with the showlist text file    
#get showlist from txt file    
def getShowList(showListFile): 
    showListDoc = open(showListFile)
    showListStr = showListDoc.read()
    showListList = showListStr.split(', ') 
    showListDoc.close()
    return showListList


def showShowList(showListFile):
    listOfShows = getShowList(showListFile)
    print(*listOfShows, sep='\n')
    
    
#add show to txt file    
def addToShowlist(nameOfShow, listOfShowsFile):
    listOfShows = getShowList(listOfShowsFile)
    if nameOfShow.title() not in listOfShows:        
        listOfShows.append(nameOfShow)
        listOfShows.sort()
        writeShowList = ", ".join(listOfShows)
        #For checking only#print(*listOfShows, sep='\n')
        #For checking only#print(writeShowList)
        showListDoc = open(listOfShowsFile, 'w')
        showListDoc.write(writeShowList)
        showListDoc.close()
        
    

    
##############
############## Selecting directories (source and output)
##############

### review to consider posting multiple path options to user with [1] [2] options for selection

#get existing directory path
def getDirectory (filePath):
    pathDoc = open(filePath)
    docPathStr = pathDoc.read()
    pathDoc.close()
    return docPathStr
    
#save directory path    
def saveDirectory (filePathDoc, filePath):
    pathDoc = open(filePathDoc, 'w')    
    pathDoc.write(filePath)
    pathDoc.close
    

def chooseDirectory (sourceOrOutput, filePathDoc):
    filePath = getDirectory(filePathDoc)

    #for new users with no director
    if filePath == '':     
        print('\nPlease input the path to the ' + sourceOrOutput + ' folder you would like to use: \n')
        filePath = input()
    
    else:
        if sourceOrOutput == "source":
            print('\nLast time you got your files from:   ')
        else:
            print('\nLast time you put your files in:   ')
        print(filePath)
        print('\nWould you like to use the same folder? [Y/N]')
        reply = getReply()
        if reply == 'n':
            print('\nPlease submit the new ' + sourceOrOutput + ' path.')
            filePath = input()
            #ensure usability of the path       
            if filePath[-1] != '/':
                filePath = ''.join((filePath,'/'))
            
            saveDirectory(filePathDoc, filePath)
            print('\nGreat! We\'ll use this path instead.')
        else:
            print ('\nGreat!')
    


#os.chdir(directoryInput + '/')


########
########Step 2: Find shows, rename them and move them
########     

def isMovieFile(fileName):
    if fileName.endswith('.mp4') or fileName.endswith('.avi') or fileName.endswith('.mpeg') or fileName.endswith('.mkv'):
        return True
    else:
        return False

    #*********Cleaning note 3 - REVIEW REGEX PROTOCOLS -> want to inclde apostrophe ',  hyphen -  and spaces in words if in the show title
    
def extractFileName(show, fileName):
     #### get showlist? from?
        titleLength = show.count(' ')

        nameRegex = re.compile(r'[a-zA-Z\ \-\']+')
        extractedName = nameRegex.findall(fileName)                
        extractedName = extractedName[0:titleLength+1]
        name = ""

        for i in extractedName:
            name = name + i + ' '

        name = name.strip()
        name = name.title()
        
        return name

def matchFileName(show, name):
    if name.lower() == show.lower():
        return True
    else:
        return False

#cleans and returns file type    
def cleanFileType(fileName):
    fileTypeRegex = re.compile(r'(\.\w{3,}$)')
    extractedFileType = fileTypeRegex.findall(fileName)
    extractedFileTypeStr = extractedFileType[0]
    return extractedFileTypeStr



##### Episode and Season Block

def cleanEpisodeAndSeason(fileName):
    episodeRegex = re.compile(r'\w\d\d\w\d\d')
    episodeRegex2 = re.compile(r'\D\d\d\d\D')    
    
    if not episodeRegex.findall(fileName):
        extractedEpisode = episodeRegex2.findall(fileName)
    else:
        extractedEpisode = episodeRegex.findall(fileName)

    extractedEpisodeStr = extractedEpisode[0]
    extractedEpisodeStr = extractedEpisodeStr.strip('.')
    
    season = whatSeason(extractedEpisodeStr)
    episode = whatEpisode(extractedEpisodeStr)
    
    extractedEpisodeStr = 'S0' + season + 'E' + episode  
    return extractedEpisodeStr

#determines season from episode and season regex extraction
def whatSeason(extractedEpisodeStr):
    season = ''
    if len(extractedEpisodeStr) == 3:
        season = extractedEpisodeStr[0]
    elif len(extractedEpisodeStr) == 6:
        season = extractedEpisodeStr[2]    
    return season

#determines episode from episode and season regex extraction
def whatEpisode(extractedEpisodeStr):
    episode = ''
    if len(extractedEpisodeStr) == 3:
        episode = extractedEpisodeStr[1:]
    elif len(extractedEpisodeStr) == 6:
        episode = extractedEpisodeStr[4:]
    return episode 


### Name and Folder block

def newFileName(show, fileName):
    newName = extractFileName(show, fileName) + " " + cleanEpisodeAndSeason(fileName) + cleanFileType(fileName)
    return newName

#def newFolderName(show fileName):
#    newFolderName = extractFileName(show, fileName) + " - Season " + whatSeason(fileName) 

def newFolderPath(outPath, fileName, newName):
    season = cleanEpisodeAndSeason(fileName)[2]
    newPath = getDirectory(outPath) + '/' + newName + '/' + newName + ' - Season ' + season + '/'
    return newPath

def moveToFolder(folderName, fileName, outPath, newFolder, newFile):
    oldPath = folderName + '/'

    if not os.path.exists(newFolder):
        os.makedirs(newFolder)
    
    shutil.move(oldPath + fileName, newFolder + newFile)
        
def cleanAndMove(inPath, outPath, showListFile):
    showlist = getShowList(showListFile)
    for folderName, subFolders, fileNames in os.walk(getDirectory(inPath)):
        for fileName in fileNames:
            if isMovieFile(fileName) == True:
                for show in showlist:
                    if matchFileName(show, extractFileName(show, fileName)) == True:
                        showName = extractFileName(show,fileName)
                        newFile = newFileName(show, fileName)
                        newFolder = newFolderPath(outPath, fileName, showName)

                        moveToFolder(folderName, fileName, outPath, newFolder, newFile)

                        print('Original file name: ' + fileName)
                        print('New file name: ' + newFile)
                        print('New file location: ' + newFolder + '\n\n')
                        



########
###Work to be done
##Bug 1: Does not work on file names that don't use . for separation (e.g. Lucha Underground)
##Task 1: Delete folders when empty 
##Task 2: Figure out how to detect the show name from the filename
##DONE -> Task 3: Add feature to add another show
