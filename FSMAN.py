#!/usr/bin/python
'''
Date: 15th Decemeber, 2021
Author: Shreesh Kumar Verma
Mail: tanaykumar103@gmail.com
Purpose: Sorts files from designated locations
'''

import os


class FileSysManager:

    # dictionary of known and common file types.
    # Helps in scaling the script to  more file types and
    # in keeping track of active file types.
    fileType = {'docx': ['docx', 'doc', 'odt', 'pdf', 'PDF',
                        'txt','xlsx', 'xls', 'csv', 'pptx', 'ppt'],
                'img': ['jpg', 'png', 'jpeg', 'svg'],
                'video': ['mkv', 'mp4', 'webm', 'flv'],
                'audio': ['mp3', 'oggs', 'flac'],
                'archive': ['xz', 'zip','rar','zst']}

    maintainedDirectories = ['$HOME/Downloads', '$HOME/Documents']
    movetoLocation = ['$HOME/Pictures', '$HOME/Documents', '$HOME/Music', '$HOME/Videos', '$HOME/Downloads/archives']
    logFileLocation = '$HOME/Documents/FS-ManagerLog.txt'
    logFileContents = ''


    '''
    Returns dictionary of files and folders as a list,
    from maintainedDirectories list.
    '''
    def DirectoryScanner(self):
        '''
        Flow of Method->
        loops through maintainedDirectories list and appends absolute path
        to dirList list. Then loops through dirList to append to values in fileDict,
        all the files and folders in dirList[x]
        '''

        dirList = []
        fileDict = {}

        for file in self.maintainedDirectories:

            # converts relative path to absolute
            dirList.append(os.path.expandvars(file))

        for dl in dirList:

            # {key: value}
            # {directory's absolute path: list of files and folders}
            fileDict[dl] = [os.path.join(dl,i) for i in os.listdir(dl)]
            
        # dictonary object of key:value as defined above
        return fileDict


    '''
    Checks for file type from fileType dictionary,
    on match takes appropriate action
    '''
    def FileTypeEvaluater(self):

        # get all maintainedDirectories and their contents with their absolute path
        mD = self.DirectoryScanner()
        
        # gives key values from mD dict
        for item in mD.keys():

            # loops over fileList given as <list> of each key's value
            for apath in range(len(mD[item])):

                # checking if current path is of a file or dir
                # if !File then skip the loop for next iteration
                # if File then carry on with operation
                if os.path.isfile(mD[item][apath]):
                    
                    # looping over fileType dict to get Key values of known filetype
                    for ftype in self.fileType:

                        # looping over filetype list provided as list of file extensions
                        for index in self.fileType[ftype]:
                            
                            # checking file extension from known filetype list
                            # if current path is in index and not in supposed directory
                            # move it to correct location
                            if mD[item][apath].endswith(index):

                                # moving the file to correct location for exception handling
                                # and reporting try has been added
                                try:
                                    self.FileMove(mD[item][apath], ftype)
                                except Exception:

                                    # adds report to self.logFileContents
                                    self.logFileContents += Exception + '\n'

        

    
    def FileMove(self, movefrom, category):
        '''
        Places files in specified location.
        Takes 2 arguments -> original location, file type.
        '''
        
        #list comprehension to get absolute path from relative path for where to place files
        #movetoLoc = [<expression> for file in <range>]
        #in this case <expreesion< is os.path.expandvars()
        #and <range> is self.movetoLocation
        movetoLoc = [os.path.expandvars(file) for file in self.movetoLocation]

        # indexed based on movetoLoc list; 
        # moves each item to indexed path in movetoLoc
        try:
            
            if category == 'docx':

                # exception added for self.logFileLocation
                # solves avoidable error
                if movefrom == os.path.expandvars(self.logFileLocation):
                    pass
                else:
                    os.system(f'mv {movefrom} {movetoLoc[1]}')
                    self.logFileContents += f"{movefrom.upper()} 'moved to' {movetoLoc[1]}"          
            
            elif category == 'img':
                os.system(f'mv {movefrom} {movetoLoc[1]}')
                self.logFileContents += f"{movefrom.upper()} 'moved to' {movetoLoc[0]}"

            elif category == 'video':
                os.system(f'mv {movefrom} {movetoLoc[1]}')
                self.logFileContents += f"{movefrom.upper()} 'moved to' {movetoLoc[3]}" 

            elif category == 'audio':
                os.system(f'mv {movefrom} {movetoLoc[1]}')
                self.logFileContents += f"{movefrom.upper()} 'moved to' {movetoLoc[2]}"

            elif category == 'archive':
                os.system(f'mv {movefrom} {movetoLoc[1]}')
                self.logFileContents += f"{movefrom.upper()} 'moved to' {movetoLoc[4]}" 

            else:
                self.logFileContents += f'{movefrom.upper()} not moved. Unknown Filetype.\n'

        except Exception as error:
            self.logFileContents += error +'\n'

    def logHandler(self):

        try:
            with open(os.path.expandvars(self.logFileLocation), 'w') as logFile:
                logFile.write(self.logFileContents)
        except FileNotFoundError as error:
            os.system(f'touch {self.logFileLocation}')
            self.logFileContents += 'LogFileNotFound hence created'
            with open(os.path.expandvars(self.logFileLocation), 'w') as logFile:
                logFile.write(self.logFileContents)



if __name__ == '__main__':
    obj = FileSysManager()
    obj.FileTypeEvaluater()
    obj.logFileContents += 'Starting FS-Manager.\n'
    obj.logHandler()