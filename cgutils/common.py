__author__ = 'aragorn'

from datetime import datetime
from pytz import utc, timezone

def localTimeString(ts=None, tz='Asia/Calcutta', tform='%Y-%m-%d %H:%M:%S'):
    loc = timezone(tz)
    utc_dt = datetime.utcnow()
    if ts:
        utc_dt = datetime.utcfromtimestamp(ts)

    loc_time = utc.localize(utc_dt, is_dst=None).astimezone(loc)

    return loc_time.strftime(tform)