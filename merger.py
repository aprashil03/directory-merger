import argparse
import shutil
import random
import sys
import os

from duplicateRemover import DuplicateRemover

class Merger:

    def __init__(self, fDir, dirList):
        self.fDir = fDir
        self.constructDirDict(dirList)

    def constructDirDict(self, dirList):
        dirDict = {}
        for directory in dirList:
            dirDict[directory] = self.getFiles(directory)
        self.dirDict = dirDict

    def getFiles(self, directory):
        return [file.name for file in os.scandir(directory)]

    def merge(self):
 
        fDir = self.fDir
        dirDict = self.dirDict

        self.handlefDir(fDir)

        for directory in dirDict:
            for file in dirDict[directory]:

                initPath = f'{directory}/{file}'
                finalPath = f'{fDir}/{file}'

                if not os.path.isfile(finalPath):
                    shutil.copyfile(initPath, finalPath)
                else:
                    self.fileExistsHandle(initPath, finalPath, file)

    def handlefDir(self, fDir):
        if not os.path.exists(fDir):
            os.makedirs(fDir)

    def fileExistsHandle(self, initPath, finalPath, file):
        f1size = os.stat(initPath).st_size
        f2size = os.stat(finalPath).st_size

        if f1size != f2size:
            name, ext = file.split('.')
            rand = random.randint(1000, 9999)
            fName = f'{self.fDir}/{name}_{rand}.{ext}'

            shutil.copyfile(initPath, fName)

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
    DRInstance = DuplicateRemover(finalDir)
    DRInstance.remover()