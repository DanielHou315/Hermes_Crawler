import os, sys
import re

import datetime, time


''' Time Related Functions '''
def two_dig(num):
    if num < 10 and num >= 0: return "0" + str(num)
    return str(num)

# Get String for a given datetime time 
def get_time_str(time):
    return str(time.year)+"_"+two_dig(time.month)+"_"+two_dig(time.day)+"_"+two_dig(time.hour)+"_"+two_dig(time.minute)+"_"+two_dig(time.second)

def get_time_str_now():
    return get_time_str(datetime.datetime.now())

def get_time_str_short(time):
    return str(time.hour) + ":" + str(time.minute)


''' Logger '''
class LogRep:
    def __init__(self, log_f="./app_log.log", print_log=False, write_log=True):
        self.log_file = log_f
        self.write = write_log
        self.print = print_log
        with open(self.log_file, 'w') as log_output:
            if self.write: log_output.write("Logger Started" + "\n")
            if self.print: print("Logger Started" + "\n")
        log_output.close()

    def log(self, src, contents):
        with open(self.log_file, 'a+') as log_output:
            if self.write: log_output.write('[' + src + '] ' + contents + "\n")
            if self.print: print('[' + src + '] ' + contents + "\n")
        log_output.close()
        


''' Filesystem Related Functions '''
def find_last_record(root):
    last_record = ""
    try:
        regex = r'Hermes_Record_.*\.html$'
        dirs = os.listdir(root+"record_cache/")
        # For Each File
        for file in dirs:
            # If it is latest record
            if(re.fullmatch(regex, file)) and file > last_record:
                last_record = file
    except:
        pass
    return last_record

def clear_cache(root):
    # try:
    last_record = find_last_record(root)
    # Clear extraneous records
    dirs = os.listdir(root + "record_cache/")
    for file in dirs:
        if file != last_record:
            os.remove(root + "record_cache/" + file)
    # Clear Image Cache
    dirs = os.listdir(root + "image_cache/")
    for file in dirs:
        os.remove(root + "record_cache/" + file) 
    return True
    # except:
    #     return False


''' Email Validator '''

def is_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False



if __name__ == "__main__":
    print("Utils Testing!")