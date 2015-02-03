from datetime import datetime
from dateutil.parser import parse as ParseDate
from dateutil.tz import tzutc
from time import time

def GetEpochUnixTime():
    epoch = datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=tzutc())
    return epoch

def GetCurrentUnixTime():
    return int(time.time() * 1000.0)

def GetUnixTime(dt):
    epoch = GetEpochUnixTime()

    if not dt.tzinfo:
        dt = dt.replace(tzinfo=tzutc())
    else:
        dt = dt.astimezone(tzutc())
    delta = dt - epoch
    return int(delta.total_seconds() * 1000.0)