from duplicateRemover import DuplicateRemover
from merger import Merger   

import argparse
import shutil
import random
import hashlib
import sys
import os

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