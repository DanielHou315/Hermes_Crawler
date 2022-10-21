import os, sys
from . import htime
# import htime

def enter_directory():
    try:
        root_dir = os.path.expanduser('~')
        if os.getcwd() == root_dir + "/Documents/.hermes_crawler/":
            return
        os.chdir(root_dir)
        if not os.path.isdir("Documents/.hermes_crawler/"):
            os.mkdir("Documents/.hermes_crawler/")
        os.chdir("Documents/.hermes_crawler/")
        return True
    except:
        return False


def find_last_record():
    if enter_directory() == False:
        return False
    last_record = ""
    try:
        for root, dirs, files in os.walk("."):
            for name in files:
                if "hermes_" in name \
                and ".html" in name \
                and "temp" not in name:
                    last_record = name
    except:
        pass
    return last_record
        

def clear_cache():
    enter_directory()
    try:
        last_record = find_last_record()
        for root, dirs, files in os.walk("."):
            for name in files:
                if "hermes_" in name \
                and name != last_record:
                    os.remove(name)
        return True
    except:
        return False


def load_email():
    enter_directory()
    email = "hermescrawlerapp@gmail.com"
    with open("setting_email.txt", 'r') as f:
        line = f.readline()
        if is_valid_email(line):
            email = line
        f.close()
    return email


def is_valid_email(email):
    if "@" in email and "." in email:
        return True
    return False


def load_history():
    enter_directory()
    last_time = "1901_1_1_0_0_0"
    time = htime.parse_time_string(last_time)
    if not os.path.isfile("setting_history.txt"):
        with open("setting_history.txt", 'w') as f:
            f.write(last_time)
            f.close()
    with open("setting_history.txt", 'r') as f:
        line = f.readline()
        time = htime.parse_time_string(line)
        f.close()
    return time


if __name__ == "__main__":
    load_history()