from .utilities.date_conversion import timestamp_to_datetime
from .utilities.date_conversion import datetime_to_date_string
from .utilities.date_conversion import timestamp_to_date_string
import datetime

def test_timestamp_to_datetime():
    timestamp = 1609553438
    assert type(timestamp_to_datetime(1609553438)) == datetime.datetime

def test_datetime_to_date_string():
    my_datetime = datetime.datetime(2021, 1, 1)
    assert datetime_to_date_string(my_datetime) == '01/01/2021'

def test_timestamp_to_date_string():
    timestamp = 1609553438
    assert timestamp_to_date_string(timestamp) == '01/01/2021'

