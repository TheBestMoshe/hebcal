from .util.proccess_time import proccess_datetime, convert_datetime_to_utc
from .util.proccess_time import convert_datetime_to_local
from .util.location import get_timezone
import ephem
from pyluach import dates
from convertdate import hebrew
from datetime import timedelta


class TimeInfo:
    def __init__(self, date_time, **kwargs):
        """Set with date_time and location info
        
        [description]
        
        Arguments:
            date_time {str} -- Valid datetime string

            accepted kwargs:
                latitude {int} -- in degrees
                longitude {int} -- in degrees
                lat_lon {tuple} -- Latitude and longitude in degrees
                timezone {str} -- A valid timezone
        
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

        self.date_time = proccess_datetime(date_time, timezone=self.timezone)

        self._sun_calculations()

        # This is used to check for halachic nightfall. The default is at
        # sunset. This can be changed, for example to 72 minutes after sunset.
        # The simplest way to do this is to create a hebcal.zmanim object and
        # use one of the nighttimes (i.e. hebcal.zmanim.Zmanim().night_72)
        if 'alternate_nighttime' in kwargs:
            self.alternate_nighttime = kwargs['alternate_nighttime']
        else:
            self.alternate_nighttime = self.today_sunset()

    def __repr__(self):
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
    
    @property
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

    @property
    def hebrew_year(self):
        """Returns the Hebrew year

        Returns:
            int -- The Hebrew year
        """

        return self.hebrew_date[0]

    @property
    def hebrew_month(self):
        """Returns the Hebrew month

        Returns:
            int -- The Hebrew month
        """

        return self.hebrew_date[1]

    @property
    def hebrew_day(self):
        """Returns the Hebrew day

        Returns:
            int -- The Hebrew day
        """

        return self.hebrew_date[2]

    @property
    def alternate_hebrew_date(self):
        """Get the day's Hebrew date if it's before the alternate_nighttime
        
        The default TimeInfo.hebrew_date bases its date on sunset. Use this
        attribute to base the Hebrew date on the alternate date
        
        Returns:
            tuple -- hebrew date formated as (year, month, day)
        """

        if self.is_night():
            if self.date_time < self.alternate_nighttime:
                date_time = self.date_time

                greg_year = int(date_time.strftime('%Y'))
                greg_month = int(date_time.strftime('%m'))
                greg_day = int(date_time.strftime('%d'))

                alternate_hebrew_date = hebrew.from_gregorian(greg_year,
                                                              greg_month,
                                                              greg_day)
            else:
                alternate_hebrew_date = self.hebrew_date
        else:
            alternate_hebrew_date = self.hebrew_date
        
        return alternate_hebrew_date

    def _sun_calculations(self):
        observer = ephem.Observer()
        observer.lat = str(self.latitude)
        observer.lon = str(self.longitude)
        observer.date = convert_datetime_to_utc(self.date_time)

        sun = ephem.Sun()
    
        observer.horizon = '0'
        # Get times from ephem
        next_sunrise = observer.next_rising(sun).datetime()
        previous_sunrise = observer.previous_rising(sun).datetime()

        next_sunset = observer.next_setting(sun).datetime()
        previous_sunset = observer.previous_setting(sun).datetime()

        observer.horizon = '-16.1'
        next_dawn = observer.next_rising(sun, use_center=True).datetime()
        previous_dawn = observer.previous_rising(sun,
                                                      use_center=True).datetime()
        
        observer.horizon = '16.1'
        next_dusk = observer.next_setting(sun, use_center=True).datetime()
        previous_dusk = observer.previous_setting(sun,
                                                       use_center=True).datetime()

        # Since the ephem times are in UTC time, convert to local time
        self.next_sunrise = convert_datetime_to_local(next_sunrise,
                                                      timezone=self.timezone)
        self.previous_sunrise = convert_datetime_to_local(previous_sunrise,
                                                          timezone=self.timezone)
        self.next_sunset = convert_datetime_to_local(next_sunset,
                                                     timezone=self.timezone)
        self.previous_sunset = convert_datetime_to_local(previous_sunset,
                                                         timezone=self.timezone)

        self.next_dawn = convert_datetime_to_local(next_dawn,
                                                   timezone=self.timezone)
        self.previous_dawn = convert_datetime_to_local(previous_dawn,
                                                       timezone=self.timezone)

        self.next_dusk = convert_datetime_to_local(next_dusk,
                                                   timezone=self.timezone)
        self.previous_dusk = convert_datetime_to_local(previous_dusk, 
                                                       timezone=self.timezone)

    def is_yom(self):
        if self.next_sunrise > self.next_sunset:
            return True
        else:
            return False
    
    def is_night(self):
        return not self.is_yom()
    
    def is_next_hebrew_day(self):
        if self.date_time.strftime('%d') == self.next_sunset.strftime('%d'):
            return False
        else:
            return True

    def today_sunrise(self):
        if self.date_time.strftime('%d') == self.previous_sunrise.strftime('%d'):
            return self.previous_sunrise
        elif self.date_time.strftime('%d') == self.next_sunrise.strftime('%d'):
            return self.next_sunrise

    def today_sunset(self):
        if self.date_time.strftime('%d') == self.previous_sunset.strftime('%d'):
            return self.previous_sunset
        elif self.date_time.strftime('%d') == self.next_sunset.strftime('%d'):
            return self.next_sunset
    
    def today_dawn(self):
        if self.date_time.strftime('%d') == self.previous_dawn.strftime('%d'):
            return self.previous_dawn
        elif self.date_time.strftime('%d') == self.next_dawn.strftime('%d'):
            return self.next_dawn

    def today_dusk(self):
        if self.date_time.strftime('%d') == self.previous_dusk.strftime('%d'):
            return self.previous_dusk
        else:
            return self.next_dusk


if __name__ == '__main__':
    i = TimeInfo.now(timezone='America/New_York',
                     latitude=40.092383, longitude=-74.219996)
    print(i.next_sunset.strftime('%-I:%M:%S %p'))
    print(i.is_yom())
    print(i.is_night())
    print(i.today_sunrise().strftime('%-I:%M:%S %p'))
    print(i.today_sunset().strftime('%-I:%M:%S %p'))
    print(i.today_dawn().strftime('%-I:%M:%S %p'))
    print(i.today_dusk().strftime('%-I:%M:%S %p'))
    print(i.hebrew_date)
    print(i.hebrew_day)
    print(i.is_next_hebrew_day())
    print(i.alternate_hebrew_date)
