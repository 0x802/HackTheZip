#!/usr/bin/python3
###################
#                 #
#  Hack The Zip   #
#                 #
###################

import os
import sys
import time
import concurrent.futures
import zipfile as _zip_

# COLORS
R = '\033[31m'
T = '\033[33m'
B = '\033[34m'
W = '\033[37m'
N = '\033[0m'


# Read File Word List 
def GET_THE_WORD_LIST(*args, **kwargs):    
    try:
        return [PASSWORD.replace(b'\n', b'') for PASSWORD in open(os.path.join(os.getcwd(), args[0]), 'rb').readlines()]
    
    except FileNotFoundError:
        print(f'[{R}!!!{N}] Sorry Not Find The Word List File ')
        sys.exit()



# Index the Secript 
def GET_THE_INDEX_SCRIPT(*args, **kwargs):
    if args[0] is True:
        # if Index One
        return f"{W}{'-'*50}{N}\n[ {B}*{N} ] Target   : {args[1]}\n[ {B}*{N} ] Word List: {args[2]}\n[ {B}*{N} ] Lines   : {len(open(args[2], 'r').readlines())}\n{W}{'-'*50}{N}\n"

    if args[0] is False:
        # if Index Files 
        print(f"[ {T}+{N} ] Find Files : ")

        for i in args[1]:print(f'----> {i} ')  
        
        input(f"\n\033[7m{B}----- Enter For (RUN) -----{N}")



# The def is process a Script : 'Find Passowrd Zip File 
def RUN_PASSWORD_IN_FILE(*args, **kwargs):
    OPEN_ZIP, PASSWORD = args[0]

    try:
        OPEN_ZIP.extractall(pwd=PASSWORD)
        print(f"[{T}<=={N}] Password : {T}{PASSWORD.decode():<5}{N} | Zip File : {W}{OPEN_ZIP.filename}{N}\n") 
        
        return True

    except Exception as e:
        print(f"[{B}==>{N}] Password : {R}{PASSWORD.decode():<5}{N} | Zip File : {W}{OPEN_ZIP.filename}{N}")
        
        return False



def GET_THE_PASSWORD_ZIP_FILE(*args, **kwargs):
    _ZIP_FILE_, _WORDLIST_, *_ = args

    # value 
    OPEN_ZIP = _zip_.ZipFile(os.path.join(os.getcwd(), _ZIP_FILE_))
    
    # list
    WORDLIST = GET_THE_WORD_LIST(os.path.join(os.getcwd(), _WORDLIST_))

    # index
    print(GET_THE_INDEX_SCRIPT(True,_ZIP_FILE_, _WORDLIST_))

    # index 2
    GET_THE_INDEX_SCRIPT(False, OPEN_ZIP.namelist())

    # Sleep 1
    time.sleep(1)

    for PASSWORD in WORDLIST:
        with concurrent.futures.ThreadPoolExecutor() as EX:
            rPASSWORD = EX.submit(RUN_PASSWORD_IN_FILE, [OPEN_ZIP, PASSWORD])
            lPASSWORD = rPASSWORD.result()
            if lPASSWORD:
                print(f"{W}{'-'*50}{N}\n{T}===>{N} The Password is {B}{PASSWORD.decode()}{N} {T}<==={N}")
                input(f"\n\033[7m{R}----- Enter For (EXIT) -----{N}")
                sys.exit(0)

            else:pass



if __name__ == "__main__":
    try:
        s, *args = sys.argv

        if len(args) != 2:
            print(f"EX:\n{s} file.zip wordlist.txt")
            exit()
        else:
            GET_THE_PASSWORD_ZIP_FILE(args[0], args[1])
        exit()
    except FileNotFoundError:
        print(f'[{R}!!!{N}] Sorry Not Find The ZIP File')
