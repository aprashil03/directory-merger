import hashlib
import os


class DuplicateRemover:

    def __init__(self, dir):
        files = self.getFiles(dir)
        checkSums = self.getCheckSums(dir, files)
        self.dir = dir
        self.zipped = [i for i in zip(files, checkSums)]

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

    def remover(self):

        dir = self.dir
        zipped = self.zipped

        iteratedElements = []
        toDelete = []

        for i in zipped:
            if i[1] in iteratedElements:
                toDelete.append(i[0])
            else:
                iteratedElements.append(i[1])

        for file in toDelete:
            os.remove(f"{dir}/{file}")
