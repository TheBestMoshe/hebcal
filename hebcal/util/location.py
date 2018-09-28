from tzwhere import tzwhere


def get_timezone(latitude, longitude):
    """Get timezone from latitude/longitude

    
    Arguments:
        lat_lon {tuple} -- latitude/longitude tuple
    
    Returns:
        str -- time zone name (i.e. America/New_York)
    """

    tz = tzwhere.tzwhere()
    return tz.tzNameAt(latitude, longitude)