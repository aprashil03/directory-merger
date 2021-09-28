import hashlib
import os


class DuplicateRemover:

    def __init__(self, dir):
        files = self.getFiles(dir)
        checkSums = self.getCheckSums(dir, files)
        self.dir = dir
        self.zipped = [i for i in zip(files, checkSums)]
        self.deletionFiles = self.prepareDeletion()

    def getFiles(self, dir):
        return [file.name for file in os.scandir(dir)]

    def getCheckSums(self, dir, files):
        checkSums = []
        for file in files:
            sha256hash = hashlib.sha256()
            with open(f"{dir}/{file}", 'rb') as f:
                sha256hash.update(f.read(4096))
            checkSums.append(sha256hash.hexdigest())
        return checkSums

    def prepareDeletion(self):

        dir = self.dir
        zipped = self.zipped

        iteratedElements = []
        toDelete = []

        for i in zipped:
            if i[1] not in iteratedElements:
                iteratedElements.append(i[1])
            else:
                toDelete.append(i)

        if toDelete:
            print("\nThe following duplicate files have been found.\n")
            _ = [print(f"[{i[0]}] {i[1]}") for i in toDelete]

        return toDelete

    def deleteFiles(self):

        dir = self.dir
        deletionFiles = self.deletionFiles

        for file in deletionFiles:
            os.remove(f"{dir}/{file[0]}")