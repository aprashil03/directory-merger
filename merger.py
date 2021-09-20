import argparse
import shutil
import random
import hashlib
import sys
import os

class Merger:

    def __init__(self, finalDir, dirList):
        self.finalDir = finalDir
        self.constructDirDict(dirList)

    def constructDirDict(self, dirList):
        dirDict = {}
        for directory in dirList:
            dirDict[directory] = self.getFileList(directory)
        self.dirDict = dirDict

    def getFileList(self, directory):
        return [file.name for file in os.scandir(directory)]

    def merge(self):
 
        finalDir = self.finalDir
        dirDict = self.dirDict

        self.handlefinalDir(finalDir)

        for directory in dirDict:
            for file in dirDict[directory]:

                initPath = f'{directory}/{file}'
                finalPath = f'{finalDir}/{file}'

                if not os.path.isfile(finalPath):
                    shutil.copyfile(initPath, finalPath)
                else:
                    self.fileExistsHandle(initPath, finalPath, file)

    # creates final dir if it doesn't exist
    def handlefinalDir(self, finalDir):
        if not os.path.exists(finalDir):
            os.makedirs(finalDir)

    # handles identical file validation
    def fileExistsHandle(self, initPath, finalPath, file):
        file1size = os.stat(initPath).st_size
        file2size = os.stat(finalPath).st_size

        if file1size != file2size:
            name, ext = file.split('.')
            rand = random.randint(1000, 9999)
            finalPath = f'{self.finalDir}/{name}_{rand}.{ext}'

            shutil.copyfile(initPath, finalPath)

        elif file1size == file2size: 
            pass
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Merge folders without worrying about duplication.')
    requiredNamed = parser.add_argument_group('Required named arguments')

    requiredNamed.add_argument('-fd', dest='final_directory', help='the final directory',required=True)
    requiredNamed.add_argument('-dir', nargs='+', dest='directories', help='the directories to be merged', required=True)
    args = parser.parse_args()

    finalDir = args.final_directory
    directories = args.directories

    MergerInstance = Merger(finalDir, directories)
    MergerInstance.merge()