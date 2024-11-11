###############################
# Circumference Over Diameter #
# A Pi calculator             #
# Version: 1.0.1              #
# Copyright (c) 2024 Te Du    #
# Licensed under Te's License #
###############################

# imports
from sys import set_int_max_str_digits, stdout
from time import sleep, time
from gmpy2 import mpz, root, get_context

# set unlimited str->int digit conversions
set_int_max_str_digits(0)

# define binary splitting algorithm
def binary_split(a: mpz, b: mpz) -> tuple[mpz, mpz, mpz]:

    # if a and b cannot be split further
    if a + 1 == b:
        Pab = -(6 * a - 5) * (2 * a - 1) * (6 * a - 1)
        Qab = 10939058860032000 * a ** 3
        Rab = Pab * (545140134 * a + 13591409)
    
    # otherwise
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)
        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb
    return Pab, Qab, Rab

# configure print() to always forcibly flush and remove newline
orig_print = print
def print(string: str) -> None:
    orig_print(string, end = "", file = print_stream, flush = True)

# define letter-by-letter printing function
def print_letter_by_letter(string: str, delay_second: bool = True) -> None:
    for i in range(len(string)):
        print(string[i])
        sleep(0.03)
    if delay_second:
        sleep(0.94)

# define variables
result = "\nPi: "
error = "\n"
print_stream = stdout

# print title
print_letter_by_letter("Circumference Over Diameter\n\nA Pi calculator\n\nVersion: 1.0.1\n\nCopyright (c) 2024 Te Du\n\nLicensed under Te's License\n\n")

# safeguard against errors
try:

    # prompt for digits
    print_letter_by_letter("How many digits would you like to calculate?", False)
    digits = int(input(" "))

    # if value is invalid, raise ValueError
    if digits < 1:
        raise ValueError
    
    # prompt for storage method
    print_letter_by_letter("\nWould you like to:\n(a) Print result to console, or \n(b) Save result to disk?", False)
    storage_choice = input(" ").lower()
    
    # if storage method is disk
    if storage_choice == "b":
        from datetime import datetime
        output_file_path = str(datetime.now()).replace(":", ".") + " - Pi.txt"
        output_file = open(output_file_path, "w")
        print_stream = output_file
        print("Circumference Over Diameter Pi file\n")
    
    # if value is invalid, raise ValueError
    elif storage_choice != "a":
        raise ValueError
    
    # start calculation timer
    start_time = time()
    
    # binary split the smallest amount of terms needed
    if digits + 4 < 14:
        Qab = 10939058860032000
        Rab = -2793657715
    else:
        Pab, Qab, Rab = binary_split(mpz(1), mpz((digits + 4) // 14 + 1))
        del Pab
    
    # set max precision for mpfr
    get_context().precision = int((digits + 4) * 3.33) + 1

    # perform final calculations and add to result
    result += str((root(10005, 2) * Qab * 426880) / (Qab * mpz(13591409) + Rab))[:digits + 2] + "\n"

    # end calculation timer
    end_time = time()

# handle invalid inputs
except ValueError:
    error += "VALUE ERROR: Invalid value."

# handle memory errors
except MemoryError:
    error += "MEMORY ERROR: Not enough memory to complete calculation."

# handle any other errors
except Exception as e:
    error += "UNKNOWN ERROR: " + str(e)

# if no error occured
if error == "\n":
    result_list = []

    # print result in intervals of 100,000
    for i in range(0, len(result), 100000):
        result_list.append(result[i:i + 100000])
    for fragment in result_list:
        print(fragment)
        sleep(0.03)
    sleep(0.94)

    # print total calculation time
    print_stream = stdout
    print_letter_by_letter("\nTotal calculation time: " + str(end_time - start_time) + " seconds\n\n")

# if an error occured, print error
else:
    print_stream = stdout
    print_letter_by_letter(error + "\n\n")

# close file if it was created, reset print stream and print file path (if applicable)
try:
    output_file.close()
    print_stream = stdout
    from os.path import abspath
    print_letter_by_letter("Pi file located at: " + abspath(output_file_path) + "\n\n")
except NameError:
    pass

# pause so the program doesn't immediately terminate
print_letter_by_letter("Press Enter to exit..", False)
input(".")