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

fileCount = 0
dirCount = 0
dupCount = 0
bytesFreed = 0
totalByteCount = 0
recursive = False

def analyseDir(dir_stack):
    while dir_stack:
        global dirCount
        dirCount += 1
        directory = dir_stack.pop()
        print(f'{bcolors.WARNING}DIRECTORY: {bcolors.ENDC}' + directory)
        print('')
        fileSizes = calculateFileSizes(directory, dir_stack)
        fileHashes1k = get1kHashes(fileSizes)
        fullHashes = getFullHashes(fileHashes1k)
        removed = removeDuplicates(fullHashes)
        global dupCount
        dupCount += removed
        if removed > 0:
            print(f'{bcolors.OKCYAN}Removed ' + str(removed) + ' duplicates from ' + 
            directory + f'{bcolors.ENDC}')
        print('-' * 120)

def calculateFileSizes(directory, dir_stack):
    fileSizes = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            if recursive:
                dir_stack.append(path)
            continue
        if os.path.islink(path):
            continue
        global fileCount
        fileCount += 1
        fileSize = os.path.getsize(path)
        global totalByteCount
        totalByteCount += fileSize
        if fileSize in fileSizes:
            fileSizes[fileSize].append(path)
        else:
            fileSizes[fileSize] = [path]
    return fileSizes

def get1kHashes(fileSizes):
    hashes1k = {}
    for size, files in fileSizes.items():
        if len(files) <= 1:
            filename = extract_filename(files[0])
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + filename + 
            ' is unique.')
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
            filename = extract_filename(files[0])
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + filename + 
            ' is unique.')
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
            filename = extract_filename(files[0])
            print(f'{bcolors.OKGREEN}UNIQUE: {bcolors.ENDC}' + filename + 
            ' is unique.')
            continue
        filename = extract_filename(files[0])
        for path in files[1:]:
            dfilename = extract_filename(path)
            print(f'{bcolors.FAIL}DUPLICATE: {bcolors.ENDC}' + dfilename + 
            ' identical to ' + filename + '. Deleting...')
            global bytesFreed
            bytesFreed += os.path.getsize(path)
            removeCount += 1
            # os.remove(path)
    return removeCount

def extract_filename(path):
    path, filename = os.path.split(path)
    return filename

# Credit - Fred Cirera at: 
# https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size
def format_bytecount(bytecount):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(bytecount) < 1024.0:
            return '%3.1f%s%s' % (bytecount, unit, 'B')
        bytecount /= 1024.0
    return '%.1f%s%s' % (bytecount, 'Yi', 'B')

def parse_args(args):
    directory = ''
    for arg in args:
        if arg == '-r':
            global recursive
            recursive = True
        else:
            if not os.path.exists(arg):
                print('Error: ' + arg + ' is not a valid directory')
                exit()
            directory = arg
    if directory == '':
        print('Error: Missing path option. Usage: python3 ' +
        'remove-duplicates.py [directory path]')
        exit()
    return directory

def main():
    directory = parse_args(sys.argv[1:])
    dir_stack = [directory]
    analyseDir(dir_stack)
    print(f'{dirCount:,d} directories traversed')
    print(format_bytecount(totalByteCount) + ' total space checked')
    print(f'{fileCount:,d} files checked')
    print(f'{dupCount:,d} duplicates found')
    print(format_bytecount(bytesFreed) + ' space freed')
    print('')
    
if __name__ == "__main__":
    main()

