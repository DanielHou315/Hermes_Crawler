import datetime, time

# Get String for a given datetime time 
def get_time_str(time):
    return str(time.year)+"_"+str(time.month)+"_"+str(time.day)+"_"+str(time.hour)+"_"+str(time.minute)+"_"+str(time.second)

def get_time_str_now():
    return get_time_str(datetime.datetime.now())

def get_time_str_short(time):
    return str(time.hour) + ":" + str(time.minute)

def get_time_str_short(time):
    return str(time.hour) + ":" + str(time.minute)

def get_relative_day_str(new_time, old_time):
    time_rel = "Today"
    if new_time.day - old_time.day < 0:
        time_rel = "In the Future"
    elif new_time.day - old_time.day == 1:
        time_rel = "Yesterday"
    elif new_time.day - old_time.day > 1:
        time_rel = str(old_time.month)+"."+str(old_time.day)
    return time_rel

def parse_time_string(time_str):
    time = datetime.datetime(1901,1,1,0,0,0)
    try:
        tmp = time_str.split("_")
        # print("Len Temp {0}".format(len(tmp)))
        if len(tmp) == 6:
            time = datetime.datetime(int(tmp[0]),int(tmp[1]),int(tmp[2]),int(tmp[3]),int(tmp[4]),int(tmp[5]))
    except:
        pass
    return time

def new_hour(new_time, old_time):
    if new_time.hour > old_time.hour \
    or new_time.day > old_time.day \
    or new_time.month > old_time.month \
    or new_time.year < old_time.year:
        return True
    return False


if __name__ == "__main__":
    o_time = parse_time_string("2022_8_23_0_50_4")
    n_time = datetime.datetime(2022,8,23,1,0,0)
    print(new_hour(o_time, n_time))
