from .util.proccess_time import proccess_datetime, convert_datetime_to_utc
from .util.proccess_time import convert_datetime_to_local
from .util.location import get_timezone
import ephem
from pyluach import dates
from convertdate import hebrew
from datetime import timedelta


class TimeInfo:
    """Container for time, date, and sun information
        
    This class is used to contain the basic information. It includes:
            - date
            - time
            - Hebrew date
            - latitude/longitude
            - timezone
            - sun times (sunrise, sunset, dawn, dusk)
            - pronunciation (ashkinazik, hebrew, etc.)
        
    """

    def __init__(self, date_time, **kwargs):
        """Setup the __init__
        
        Args:
            date_time {str} -- Valid datetime string

            accepted kwargs:
                latitude {int} -- in degrees
                longitude {int} -- in degrees
                lat_lon {tuple} -- Latitude and longitude in degrees
                timezone {str} -- A valid timezone
                pronunciation {str} -- Pronunciation to use. Accepted values
                    are: american_ashkinazik
        
        Attributes:
            latitude (float): The latitude
            longitude (float): The longitude
            timezone (str): The timezone
            datetime (:obj:): The datetime
            alternate_nighttime (:obj:): An alternate nighttime to use for
                some calculations
        
        Raises:
            Exception -- If no location info is given
        """

        if 'latitude' in kwargs and 'longitude' in kwargs:
            latitude = kwargs['latitude']
            longitude = kwargs['longitude']
        elif 'lat_lon' in kwargs:
            latitude = kwargs['lat_lon'][0]
            longitude = kwargs['lat_lon'][1]
        else:
            raise Exception('A latitude and longitude is required.')

        self.latitude = latitude
        self.longitude = longitude

        if 'timezone' in kwargs:
            timezone = kwargs['timezone']
        else:
            # using get_timezone() slows is slow. It's better to pass in a
            # timzone argument when creating TimeInfo()
            timezone = get_timezone(self.latitude, self.longitude)

        self.timezone = timezone

        # self.date_time = proccess_datetime(date_time, timezone=self.timezone)
        self.date_time = date_time

        # This is used to check for halachic nightfall. The default is at
        # sunset. This can be changed, for example to 72 minutes after sunset.
        # The simplest way to do this is to create a hebcal.zmanim object and
        # use one of the nighttimes (i.e. hebcal.zmanim.Zmanim().night_72)
        if 'alternate_nighttime' in kwargs:
            self.alternate_nighttime = kwargs['alternate_nighttime']
        else:
            self.alternate_nighttime = self.today_sunset
        
        # Set the pronunciation that will be used.
        # If no value is set, the default will be "american_ashkinazik"
        if 'pronunciation' in kwargs:
            valid_pronuncitation = ['american_ashkinazik']
            if kwargs['pronunciation'] in valid_pronuncitation:
                self.pronunciation = kwargs['pronuncitation']
            else:
                raise Exception(f"pronunciation={kwargs['pronunciation']} is"
                                " invalid")
        else:
            self.pronunciation = 'american_ashkinazik'

    @property
    def date_time(self):
        """ Returns a date_time object """
        return self._date_time_object

    @date_time.setter
    def date_time(self, date_time):
        """ Parse a datetime object or string """
        self._date_time_object = proccess_datetime(date_time,
                                                   timezone=self.timezone)

    def __repr__(self):
        """ Returns the current a string of a fully reproducible class info """
        return (f"hebcal.TimeInfo('{str(self.date_time)}', "
                f"latitude={self.latitude}, longitude={self.longitude}, "
                f"timezone={self.timezone})")

    @classmethod
    def now(cls, **kwargs):
        """Call class with current time and date

        Returns:
            cls -- Instance of the class with the current time and date
        """

        from datetime import datetime
        return cls(datetime.now(), **kwargs)
    
    def hebrew_date(self):
        """Return the Hebrew date as a tuple
        
        Returns:
            tuple -- Hebrew date (year, month, day)
        """

        if self.is_night():
            date_time = self.date_time + timedelta(days=1)
        else:
            date_time = self.date_time
        greg_year = int(date_time.strftime('%Y'))
        greg_month = int(date_time.strftime('%m'))
        greg_day = int(date_time.strftime('%d'))

        return hebrew.from_gregorian(greg_year, greg_month, greg_day)

    def hebrew_year(self):
        """Returns the Hebrew year

        Returns:
            int -- The Hebrew year
        """

        return self.hebrew_date()[0]

    def hebrew_month(self):
        """Returns the Hebrew month

        Returns:
            int -- The Hebrew month
        """

        return self.hebrew_date()[1]

    def hebrew_day(self):
        """Returns the Hebrew day

        Returns:
            int -- The Hebrew day
        """

        return self.hebrew_date()[2]

    def alternate_hebrew_date(self):
        """Get the day's Hebrew date if it's before the alternate_nighttime

        The default TimeInfo.hebrew_date bases its date on sunset. Use this
        attribute to base the Hebrew date on the alternate date

        Returns:
            tuple -- hebrew date formated as (year, month, day)
        """

        if self.is_night():
            if self.date_time < self.alternate_nighttime():
                date_time = self.date_time

                greg_year = int(date_time.strftime('%Y'))
                greg_month = int(date_time.strftime('%m'))
                greg_day = int(date_time.strftime('%d'))

                alternate_hebrew_date = hebrew.from_gregorian(greg_year,
                                                              greg_month,
                                                              greg_day)
            else:
                alternate_hebrew_date = self.hebrew_date()
        else:
            alternate_hebrew_date = self.hebrew_date()

        return alternate_hebrew_date

    def _setup_sun(self):
        """Setup for sun calculations
        
        Builds PyEphem objects to calculate the sun times
        
        Returns:
            Obj: Returns an ephem.Observer() object and a ephem.Sun() object
        """

        observer = ephem.Observer()
        observer.lat = str(self.latitude)
        observer.lon = str(self.longitude)
        observer.date = convert_datetime_to_utc(self.date_time)
        sun = ephem.Sun()

        return observer, sun
    
    @property
    def next_sunrise(self):
        """ Return the time for the next sunrise """
        observer, sun = self._setup_sun()
        next_sunrise = observer.next_rising(sun).datetime()
        return convert_datetime_to_local(next_sunrise, timezone=self.timezone)
    
    @property
    def previous_sunrise(self):
        """ Return the time for the previous sunrise """
        observer, sun = self._setup_sun()
        previous_sunrise = observer.previous_rising(sun).datetime()
        return convert_datetime_to_local(previous_sunrise,
                                         timezone=self.timezone)
    
    @property
    def next_sunset(self):
        """ Return the time for the next sunset """
        observer, sun = self._setup_sun()
        next_sunset = observer.next_setting(sun).datetime()
        return convert_datetime_to_local(next_sunset, timezone=self.timezone)
    
    @property
    def previous_sunset(self):
        """ Return the time for the previous sunset """
        observer, sun = self._setup_sun()
        previous_sunset = observer.previous_setting(sun).datetime()
        return convert_datetime_to_local(previous_sunset,
                                         timezone=self.timezone)
    
    @property
    def next_dawn(self):
        """ Return the time for the next dawn 
        
        This dawn is calculated when the sun is 16.1° before sunrise (-16.1)
        """
        observer, sun = self._setup_sun()
        observer.horizon = '-16.1'
        next_dawn = observer.next_rising(sun, use_center=True).datetime()
        return convert_datetime_to_local(next_dawn, timezone=self.timezone)
    
    @property
    def previous_dawn(self):
        """ Return the time for the previous dawn

        This dawn is calculated when the sun is 16.1° before sunrise (-16.1)
        """
        observer, sun = self._setup_sun()
        observer.horizon = '-16.1'
        previous_dawn = observer.previous_rising(sun,
                                                 use_center=True).datetime()
        return convert_datetime_to_local(previous_dawn, timezone=self.timezone)

    def is_day(self):
        """Check if its currently day
        
        Returns:
            True if its day. False it its night
        """

        if self.next_sunrise > self.next_sunset:
            return True
        else:
            return False
    
    def is_night(self):
        """Check if its currently night
    
        Returns:
            True if its day. False if its night
        """

        return not self.is_day()
    
    def is_next_hebrew_day(self):
        """Check if it's already the next Hebrew day
        
        The hebrew day begins at sunset. Therefore, if it's after sunset, the
        the next Hebrew day has begun. This will return True if the next Hebrew
        day has begun.
        
        Returns:
            True if the next hebrew day has begun. False otherwise
        """

        if self.date_time.strftime('%d') == self.next_sunset.strftime('%d'):
            return False
        else:
            return True

    def today_sunrise(self):
        """Get the sunrise of the current day
        
        Returns:
            object: datetime.datetime object of the sunrise time
        """

        if self.date_time.strftime('%d') == self.previous_sunrise.strftime('%d'):
            return self.previous_sunrise
        elif self.date_time.strftime('%d') == self.next_sunrise.strftime('%d'):
            return self.next_sunrise

    def today_sunset(self):
        """Get the sunset of the current day
        
        Returns:
            object: datetime.datetime object of the sunset time
        """

        if self.date_time.strftime('%d') == self.previous_sunset.strftime('%d'):
            return self.previous_sunset
        elif self.date_time.strftime('%d') == self.next_sunset.strftime('%d'):
            return self.next_sunset
    
    def today_dawn(self):
        """Get the dawn of the current day
        
        This is the Alot Hashsachar calculated with -16.1 degrees
        
        Returns:
            object: datetime.datetime object of the time of dawn
        """

        if self.date_time.strftime('%d') == self.previous_dawn.strftime('%d'):
            return self.previous_dawn
        elif self.date_time.strftime('%d') == self.next_dawn.strftime('%d'):
            return self.next_dawn
