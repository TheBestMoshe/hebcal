class Calendar:
    def __init__(self, info):
        self.hebrew_month = str(info.hebrew_month())
        self.hebrew_day = str(info.hebrew_day())

        self.rest_holidays = {
            '1': {
                '15': ['passover', 1],
                '16': ['passover', 2],

                '21': ['passover', 7],
                '22': ['passover', 8],
                },
            '3': {
                '6': ['shavuot', 1],
                '7': ['shavuot', 2],
                },
            '7': {
                '1': ['rosh hashana', 1],
                '2': ['rosh hashana', 2],
                '10': ['yom kippur', 0],
                '15': ['sukkot', 1],
                '16': ['sukkot', 2],

                '22': ['shminiatzeres', 0],
                '23': ['simchastorah', 0],
            }
                              }

        self.work_holiday = {
            '1': {
                '17': ['passover chol hamoed', 1],
                '18': ['passover chol hamoed', 2],
                '19': ['passover chol hamoed', 3],
                '20': ['passover chol hamoed', 4],
            },
            '2': {
                '14': ['pesach sheni', 0],
                '18': ['lag baomer', 0],
            },
            '7': {
                '17': ['sukkot chol hamoed', 1],
                '18': ['sukkot chol hamoed', 2],
                '19': ['sukkot chol hamoed', 3],
                '20': ['sukkot chol hamoed', 4],
                '21': ['sukkot hoshana raba', 0],
            },
            '9': {
                '24': ['erev hanukah'],
                '25': ['hanukah', 1],
                '26': ['hanukah', 2],
                '27': ['hanukah', 3],
                '28': ['hanukah', 4],
                '29': ['hanukah', 5],
                '30': ['hanukah', 6],
                '1': ['hanukah', 7],
                '2': ['hanukah', 8],
            },
        }
    
    def get_rest_holiday(self):
        """Get the rest holiday if it exists. Otherwise it returns None
        
        Returns:
            list -- Returns a list contianing the holiday info. Returns None
                    if there is no holiday
        """

        if self.hebrew_month in self.rest_holidays:
            if self.hebrew_day in self.rest_holidays[self.hebrew_month]:
                return self.rest_holidays[self.hebrew_month][self.hebrew_day]
        return None
    
    def get_work_holiday(self):
        """Get the work holiday if it exists. Otherwise it returns None
        
        Returns:
            list -- Returns a list contianing the holiday info. Returns None
                    if there is no holiday
        """

        if self.hebrew_month in self.work_holiday:
            if self.hebrew_day in self.work_holiday[self.hebrew_month]:
                return self.work_holiday[self.hebrew_month][self.hebrew_day]
        return None
    
    @classmethod
    def is_holiday(cls, info):
        """Checks if there is a holiday
        
        If there is a rest or work holiday it will return True. Otherwise it 
        will be false
        
        Arguments:
            info {object} -- A hebcal.TimeInfo object
        
        Returns:
            boolean -- True if its a holiday False if its not a holiday
        """

        holidays = cls(info)

        if holidays.get_rest_holiday() is not None:
            return True

        if holidays.get_work_holiday() is not None:
            return True

        return False

    @classmethod
    def is_rest_holiday(cls, info):
        """Returns True if its a rest holiday
        
        Checks if its a rest holiday. By default its calculated from sunset to
        sunset. If you set TimeInfo.alternate_nighttime to a diffrent time, it
        will calculate from sunset to TimeInfo.alternate_nighttime
        
        Arguments:
            info {object} -- hebcal.TimeInfo object
        
        Returns:
            bool -- True if its a rest holiday False if it's not.
        """

        holiday = cls(info)

        if holiday.get_rest_holiday() is not None:
            return True

        else:
            if info.alternate_hebrew_date() != info.hebrew_date():
                holiday.hebrew_month = str(info.alternate_hebrew_date()[1])
                holiday.hebrew_day = str(info.alternate_hebrew_date()[2])

                if holiday.get_rest_holiday() is not None:
                    return True
        return False

    @staticmethod
    def is_shabbos(info):
        """Check if the current datetime is Shabbos
        
        Arguments:
            info {[type]} -- A HebCal TimeInfo object

        Returns:
            [bool] -- True if its Shabbos
        """

        # See if its Friday night
        if info.date_time.weekday() == 4:
            if info.is_next_hebrew_day():
                return True
    
        # See if its Saturday
        if info.date_time.weekday() == 5:

            # Use the alternate nighttime to allow for adjustments for halachic
            #   nighttime (e.g. Use Rabinu Tam zman, whcich is 72 minutes after
            #   sunset)
            night = info.alternate_nighttime
            if info.date_time < night:
                return True

        return False

    @classmethod
    def is_today_rest_day(cls, info):
        holidays = cls(info)

        if holidays.get_rest_holiday() is not None:
            return True

        if self.is_shabbos(info):
            return True

        return False


if __name__ == '__main__':
    from __init__ import TimeInfo
    from datetime import timedelta
    from zmanim import Zmanim

    ti = TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
                  latitude=40.092383, longitude=-74.219996)
    # ti = TimeInfo.now(timezone='America/New_York',
    #                   latitude=40.092383, longitude=-74.219996)
    # print(Holidays.is_today_holiday(ti))
    z = Zmanim(ti)
    print(z)
    ti.alternate_nighttime = z.night_72
    # ti.heb_date()
    # print(Holidays.is_shabbos(ti))
    print(Holidays.is_rest_holiday(ti))
    print(ti.hebrew_date, 'hebrew date')
    print(ti.alternate_hebrew_date(), 'alternate')
