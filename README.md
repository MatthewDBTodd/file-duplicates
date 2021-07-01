# file-duplicates

Python script to traverse the file system and locate file duplicates. For efficiency it first uses file sizes to find duplicates, then as a second phase it uses file hashes to compare any files of the same size to determine if the files are duplicates.

You can either search the current directory only, or pass in the -r command line argument for it to search recursively.

Currently I've commented out the line which actually removes the duplicates, mainly for safety reasons. I still need to add options to only search for certain file-types.
