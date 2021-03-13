import os
import hashlib
from shutil import copyfile

dir1 = 'Folder 1 Surplus'
dir2 = 'Folder 2 Deficit'
destinationDirectory = 'merged'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def hashDirectory(directory):
    hashes = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        filehash = hash(path)
        hashes[filehash] = path 
    return hashes

def hash(filename):
    BLOCKSIZE = 65536
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        data = f.read(BLOCKSIZE)
        while len(data) > 0:
            md5.update(data)
            data = f.read(BLOCKSIZE)
        return md5.hexdigest()

def getpath(filename):
    path, filename_ = os.path.split(filename)
    return os.path.join(destinationDirectory, filename_)

def copydirectory(src, dest):
    count = 0
    for filename in os.listdir(src):
        srcpath = os.path.join(src, filename)
        destpath = os.path.join(dest, filename)
        print('Copying ' + srcpath + ' to ' + destpath)
        copyfile(srcpath, destpath)
        count += 1
    return count

def main():
    dir1_hashes = hashDirectory(dir1)
    dir2_hashes = hashDirectory(dir2)
    
    duplicateCount = 0
    uniqueCount = 0
    for key, value in dir2_hashes.items():
        if key in dir1_hashes:
            print(f'{bcolors.WARNING}DUPLICATE {bcolors.ENDC}' + value + ' already in ' + dir1 + ', skipping')
            duplicateCount += 1
        else:
            print(f'{bcolors.OKGREEN}UNIQUE {bcolors.ENDC}' + value + ' not in ' + dir1 + '. Copying...')
            newpath = getpath(value)
            copyfile(value, newpath)
            uniqueCount += 1

    print('-' * 100)
    print(str(uniqueCount) + ' unique files found in ' + dir2 + ', ' + str(duplicateCount) + ' duplicates skipped.')

if __name__ == "__main__":
    main()
