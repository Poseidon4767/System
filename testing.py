def getDateTime():
    import datetime
    return datetime.datetime.now().date(), datetime.datetime.now().time()
    
def formatDateTime():
    date, time = getDateTime()
    hour = time.hour
    minute = time.minute
    second = time.second
    date_str = str(date)
    time_str = str(hour) + ":" + str(minute) + ":" + str(second)
    print(f"[{date_str} {time_str}]")

formatDateTime()