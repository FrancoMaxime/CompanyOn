import hashlib
import binascii
import math
import time
import datetime

datetimeformat = "%Y-%m-%d %H:%M:%S"

def get_timestamp():
    now = time.time()
    now = math.floor(float(now))
    now = int(now)
    return now


def encrypt(password, salt):
    sha = hashlib.pbkdf2_hmac('sha256', password, salt, 126425)
    return binascii.hexlify(sha)


def timestamp_to_date(now, format=datetimeformat):
    return datetime.datetime.fromtimestamp(int(now)).strftime(format)


def timestamp_to_time(now):
    return str(datetime.timedelta(seconds=now))


def get_time():
    now = int(time.time())
    return datetime.datetime.fromtimestamp(now).strftime(datetimeformat)

def date_to_timestamp(date):
    try:
        tmp = datetime.datetime.strptime(date, datetimeformat)
    except:  # old format ?
        tmp = datetime.datetime.strptime(date, "%H:%M:%S  -  %d/%m/%y")
    return (tmp - datetime.datetime(1970, 1, 1)).total_seconds()


def transform_date(date):
    try:
        tmp = datetime.datetime.strptime(date, datetimeformat).isoformat()
    except:  # old format ?
        tmp = datetime.datetime.strptime(date, "%H:%M:%S  -  %d/%m/%y").isoformat()
    return tmp


def now():
    return unicode(datetime.datetime.now().strftime(datetimeformat))
