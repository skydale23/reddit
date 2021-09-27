import datetime
import pytz

def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def convert_timezone(datetime, start = pytz.utc, end = pytz.timezone('US/Eastern')):
    return datetime.astimezone()

def datetime_to_date_string(datetime, format_code = "%m/%d/%Y"):
    return datetime.strftime(format_code)

def timestamp_to_date_string(timestamp, format_code = "%m/%d/%Y"):
    dt = timestamp_to_datetime(timestamp)
    date_string = datetime_to_date_string(dt, format_code = format_code)
    return date_string


