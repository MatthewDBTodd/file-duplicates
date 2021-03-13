#!/usr/bin/env python3

import os
import hashlib
import sys

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'

def analyseDir(dir_stack):
    while dir_stack:
        directory = dir_stack.pop()
        print(f'{bcolors.WARNING}DIRECTORY: {bcolors.ENDC}' + directory)
        fileSizes = calculateFileSizes(directory, dir_stack)
        fileHashes1k = get1kHashes(fileSizes)
        fullHashes = getFullHashes(fileHashes1k)
        removed = removeDuplicates(fullHashes)
        print(f'{bcolors.OKCYAN}Removed ' + str(removed) + ' duplicates from ' + directory + f'{bcolors.ENDC}')
        print('-' * 200)

def calculateFileSizes(directory, dir_stack):
    fileSizes = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            dir_stack.append(path)
            continue
        if os.path.islink(path):
            continue
        fileSize = os.path.getsize(path)
        if fileSize in fileSizes:
            fileSizes[fileSize].append(path)
        else:
            fileSizes[fileSize] = [path]
    return fileSizes

def get1kHashes(fileSizes):
    hashes1k = {}
    for size, files in fileSizes.items():
        if len(files) <= 1:
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + files[0] + ' no identical filesize found.')
            continue
        for filename in files:
            sha1 = hashlib.sha1()
            with open(filename, 'rb') as f:
                sha1.update(f.read(1024))
                hash1k = sha1.hexdigest()
                if hash1k in hashes1k:
                    hashes1k[hash1k].append(filename)
                else:
                    hashes1k[hash1k] = [filename]
    return hashes1k

def getFullHashes(hashes1k):
    hashes = {}
    for hash1k, files in hashes1k.items():
        if len(files) <= 1:
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + files[0] + ' no identical 1k hash found.')
            continue
        for filename in files:
            filehash = hash(filename)
            if filehash in hashes:
                hashes[filehash].append(filename)
            else:
                hashes[filehash] = [filename]
    return hashes

def hash(filename):
    BLOCKSIZE = 65536
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        data = f.read(BLOCKSIZE)
        while len(data) > 0:
            sha1.update(data)
            data = f.read(BLOCKSIZE)
        return sha1.hexdigest()

def removeDuplicates(hashes):
    removeCount = 0
    for filehash, files in hashes.items():
        if len(files) <= 1:  
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + files[0] + ' no identical full hash found.')
            continue
        filename = files[0]
        for path in files[1:]:
            print(f'{bcolors.FAIL}DUPLICATE: {bcolors.ENDC}' + path + ' identical to ' + filename + '. Deleting...')
            removeCount += 1
            # os.remove(path)
    return removeCount

def main():
    if len(sys.argv) != 2:
        print('Error: Missing path option. Usage: python3 remove-duplicates.py [directory path]')
        exit()
    if not os.path.exists(sys.argv[1]):
        print('Error: ' + sys.argv[1] + ' is not a valid directory')
        exit()
    dir_stack = [sys.argv[1]]
    analyseDir(dir_stack)
    
if __name__ == "__main__":
    main()

