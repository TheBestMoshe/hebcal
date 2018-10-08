american_ashkinazik_holidays = {
            'passover': 'Pesach',
            'passover_chol_hamoed': 'Chol Hamoed Pesach',
            'shavuot': 'Shavuos',
            'rosh_hashana': 'Rosh Hashana',
            'yom_kippur': 'Yom Kippur',
            'sukkot': 'Sukkos',
            'sukkot_chol_hamoed': 'Chol Hamoed Sukkos',
            'hoshana_raba': 'Hoshana Raba',
            'shemini_atzeret': 'Shmini Atzeres',
            'simchat_torah': 'Simchas Torah',
            'pesach_sheni': 'Pesach Sheini',
            'lag_baomer': "Lag Ba'omer",
            'hanukah': 'Chanuka'
            }


class Holiday:
    def __init__(self, info):
        self.info = info
        self.hebrew_month = str(self.info.hebrew_month())
        self.hebrew_day = str(self.info.hebrew_day())
    
    @property
    def rest_holidays(self):
        holiday_name = self.holiday_pronunciation_dict()

        rest_holidays = {
            '1': {
                '15': [holiday_name['passover'], 1],
                '16': [holiday_name['passover'], 2],
                '21': [holiday_name['passover'], 7],
                '22': [holiday_name['passover'], 8],
                },
            '3': {
                '6': [holiday_name['shavuot'], 1],
                '7': [holiday_name['shavuot'], 2],
                },
            '7': {
                '1': [holiday_name['rosh_hashana'], 1],
                '2': [holiday_name['rosh_hashana'], 2],
                '10': [holiday_name['yom_kippur'], 0],
                '15': [holiday_name['sukkot'], 1],
                '16': [holiday_name['sukkot'], 2],

                '22': [holiday_name['shemini_atzeret'], 0],
                '23': [holiday_name['simchat_torah'], 0],
            }
        }
        return rest_holidays
    
    @property
    def work_holiday(self):
        holiday_name = self.holiday_pronunciation_dict()

        work_holiday = {
            '1': {
                '17': [holiday_name['passover_chol_hamoed'], 1],
                '18': [holiday_name['passover_chol_hamoed'], 2],
                '19': [holiday_name['passover_chol_hamoed'], 3],
                '20': [holiday_name['passover_chol_hamoed'], 4],
            },
            '2': {
                '14': [holiday_name['pesach_sheni'], 0],
                '18': [holiday_name['lag_baomer'], 0],
            },
            '7': {
                '17': [holiday_name['sukkot_chol_hamoed'], 1],
                '18': [holiday_name['sukkot_chol_hamoed'], 2],
                '19': [holiday_name['sukkot_chol_hamoed'], 3],
                '20': [holiday_name['sukkot_chol_hamoed'], 4],
                '21': [holiday_name['hoshana_raba'], 0],
            },
            '9': {
                '24': ['erev hanukah'],
                '25': [holiday_name['hanukah'], 1],
                '26': [holiday_name['hanukah'], 2],
                '27': [holiday_name['hanukah'], 3],
                '28': [holiday_name['hanukah'], 4],
                '29': [holiday_name['hanukah'], 5],
                '30': [holiday_name['hanukah'], 6],
                '1': [holiday_name['hanukah'], 7],
                '2': [holiday_name['hanukah'], 8],
            },
        }
        return work_holiday

    def holiday_pronunciation_dict(self):
        if self.info.pronunciation == 'american_ashkinazik':
            return american_ashkinazik_holidays

        # TODO: add other pronunciation options

        else:
            return american_ashkinazik_holidays

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
    

def is_holiday(info):
    """Checks if there is a holiday
    
    If there is a rest or work holiday it will return True. Otherwise it 
    will be false
    
    Arguments:
        info {object} -- A hebcal.TimeInfo object
    
    Returns:
        boolean -- True if its a holiday False if its not a holiday
    """

    holidays = Holiday(info)

    if holidays.get_rest_holiday() is not None:
        return True

    if holidays.get_work_holiday() is not None:
        return True

    return False


def is_rest_holiday(info):
    """Returns True if its a rest holiday

    Checks if its a rest holiday. By default its calculated from sunset to
    sunset. If you set TimeInfo.alternate_nighttime to a diffrent time, it
    will calculate from sunset to TimeInfo.alternate_nighttime

    Arguments:
        info {object} -- hebcal.TimeInfo object

    Returns:
        bool -- True if its a rest holiday False if it's not.
    """

    holiday = Holiday(info)

    if holiday.get_rest_holiday() is not None:
        return True

    else:
        if info.alternate_hebrew_date() != info.hebrew_date():
            holiday.hebrew_month = str(info.alternate_hebrew_date()[1])
            holiday.hebrew_day = str(info.alternate_hebrew_date()[2])

            if holiday.get_rest_holiday() is not None:
                return True
    return False


def is_rest_day(info):
    holidays = Holiday(info)

    if holidays.get_rest_holiday() is not None:
        return True

    if is_shabbos(info):
        return True

    return False


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
