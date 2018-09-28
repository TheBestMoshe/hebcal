from dateutil.parser import parse, parserinfo
import pytz
import datetime


def proccess_datetime(raw_datetime, **kwargs):
    """Proccess a datetime string or object
    
    Convert a datetime string into a datetime object and adds UTC timzone
    offset to the datetime
    
    Arguments:
        raw_datetime {str/datetime.datetime} -- datetime string in 
        {YYYY-MM-DD HH-MM-SS} format.
        
        **kwargs {key word arguments} -- Valid keyword arguments are:
              timezone {str} -- valid pytz timezone (i.e. America/New_York)
    
    Returns:
        datetime.datetime object -- datetime object including localization info
    """

    if isinstance(raw_datetime, datetime.datetime):
        proccessed_datetime = raw_datetime
    else:
        proccessed_datetime = parse_datetime_str(raw_datetime)
    
    if 'timezone' in kwargs:
        proccessed_datetime = add_timezone_to_datetime(proccessed_datetime,
                                                       kwargs['timezone'])
    return proccessed_datetime


def parse_datetime_str(raw_datetime):
    """Parse a datetime string
    
    use dateutil.parser.parse to parse a datetime string
    
    Arguments:
        raw_datetime {str} -- datetime string in {YYYY-MM-DD HH-MM-SS} format.
                              other formats may also work.
    
    Returns:
        object -- datetime.datetime object
    """
    return parse(raw_datetime)


def add_timezone_to_datetime(datetime, timezone):
    return datetime.astimezone(pytz.timezone(timezone))


def convert_datetime_to_utc(datetime):
    return datetime.astimezone(pytz.UTC)


def convert_datetime_to_local(date_time, timezone):
    return date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))


if __name__ == '__main__':
    now = datetime.datetime.now()
    print(now)
    now = convert_datetime_to_utc(now)
    print(now)
    print(proccess_datetime('2018 9, 13, 5:56PM'))