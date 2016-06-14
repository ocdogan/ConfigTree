import time
from datetime import datetime

def Local2UTC(local_time):
    epoch_second = time.mktime(local_time.timetuple())
    return datetime.utcfromtimestamp(epoch_second)

from dateutil import tz

__local_time_zone = tz.tzlocal()

def asUtc(dt):
    epoch_second = time.mktime(dt.timetuple())
    dt = datetime.utcfromtimestamp(epoch_second).replace(microsecond=dt.microsecond)
    dt = dt.replace(tzinfo=tz.tzlocal())
    return dt.isoformat()

d = Local2UTC(datetime.now())
print d
print d.tzinfo
print d.utctimetuple()

from time import strftime, gmtime, localtime

print strftime('%H:%M:%S', gmtime()) #UTC time
print strftime('%H:%M:%S', localtime()) # localtime

now = datetime.utcnow()
from dateutil import tz
HERE = tz.tzlocal()
UTC = tz.gettz('UTC')

# The Conversion:
gmt = now.replace(tzinfo=UTC)
print gmt
print gmt.astimezone(HERE)
print datetime.utcnow().replace(tzinfo=tz.tzlocal()).isoformat()
print asUtc(datetime.now())
