import sys
import os

if len(sys.argv) is not 2:
    print("Plese Use like ./bin_to_raw.py <file_name>")
    exit(-1)

file_name = "./"+sys.argv[1]
raw_file_name = file_name[:-4]+".raw"
"""
arr = open(file_name, "r").read().split(",")
arr = list(map(int, arr))
f = open(raw_file_name[:-4], "wb")
newByteArr = bytearray(arr)
f.write(newByteArr)
f.close()
"""
os.system('./convert -f '+sys.argv[1])
