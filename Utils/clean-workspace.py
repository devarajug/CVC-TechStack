from os import remove
from os import sep
from os import listdir
from os.path import join
from os.path import isdir
from sys import argv

output_dir = argv[1].split("\\")
output_dir.insert(1, sep)

try:
    if isdir(join(*output_dir)):
        for file in listdir(join(*output_dir)):
            remove(join(*output_dir, file))
except Exception as e:
    print(e)