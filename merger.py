import argparse
import shutil
import random
import hashlib
import sys
import os

from duplicateRemover import DuplicateRemover

class Merger:

    def __init__(self, finalDir, dirList, hashsize=4098):
        self.finalDir = finalDir
        self.hashsize = hashsize
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
                    self.logging(initPath, "No verification needed.")

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
            self.copyDuplicate(file, initPath, finalPath)
            self.logging(initPath, "file size")


        elif file1size == file2size: 

            filehashes = {}

            sha256hash = hashlib.sha256()
            with open(initPath, 'rb') as f:
                sha256hash.update(f.read(self.hashsize))
            filehashes["file1hash"] = sha256hash.hexdigest()

            sha256hash = hashlib.sha256()
            with open(finalPath, 'rb') as f:
                sha256hash.update(f.read(self.hashsize))
            filehashes["file2hash"] = sha256hash.hexdigest()

            if filehashes["file2hash"] != filehashes["file1hash"]:
                self.copyDuplicate(file, initPath, finalPath)
                self.logging(initPath, "sha256 checksum")
            else:
                pass
        
    def copyDuplicate(self, file, initPath, finalPath):
        name, ext = file.split('.')
        rand = random.randint(1000, 9999)
        finalPath = f'{self.finalDir}/{name}_{rand}.{ext}'

        shutil.copyfile(initPath, finalPath)

    def logging(self, initPath, verification):
        print(f"Successfully Copied {initPath} | verification used: {verification}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Merge folders without worrying about duplication.')
    requiredNamed = parser.add_argument_group('Required named arguments')

    requiredNamed.add_argument('-fd', dest='final_directory', help='the final directory',required=True)
    requiredNamed.add_argument('-dir', nargs='+', dest='directories', help='the directories to be merged', required=True)

    requiredNamed = parser.add_argument_group('Optional Arguments')
    requiredNamed.add_argument('-hs', dest='hashsize', help='sha256hash bit size', type=int, required=False)
    requiredNamed.add_argument('-rd', action="store_true", dest='removedup', help='remove duplicates', required=False)

    args = parser.parse_args()

    finalDir = args.final_directory
    directories = args.directories
    hashsize = args.hashsize
    removeDup = args.removedup

    MergerInstance = Merger(finalDir, directories, hashsize)
    MergerInstance.merge()

    DuplicateRemoverInstance = DuplicateRemover(finalDir)

    if removeDup:
        DuplicateRemoverInstance.deleteFiles()
        print("\nDuplicate files have been deleted.")