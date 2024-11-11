#########################################
# Get last 100 characters of a txt file #
# Used for verifying digits of pi       #
# Copyright (c) 2024 Te Du              #
# Licensed under Te's License           #
#########################################

# prompt for file location
file_path = input("Enter full (absolute) file path to check: ")

# try to open file
try:
    txt_file = open(file_path, "r")
except:
    print("\nERROR: Couldn't open file \"" + file_path + "\"")
    exit(1)

# read last 100 chars
print("\nLast 100 chars: \"" + txt_file.read()[-100:].replace("\n", "\\n") + "\"")