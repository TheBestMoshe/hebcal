import hebcal


# This datetime that is used, is after sunset of Yom Kippur (sunset is 6:59 PM)
# In this test we will test alternate nighttimes as well, which should then
# still be Yom Kippur.

list_of_times = [{'datetime': '2018, 9, 19, 7:15 pm',
                  'use_alternate_nighttime': False,
                  'get_rest_holiday': None,
                  'get_work_holiday': None,
                  'is_holiday': False,
                  'is_rest_holiday': False,
                  'is_shabbos': False},
                 ]

ti = hebcal.TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
                     latitude=40.092383, longitude=-74.219996)

holiday = hebcal.calendar.Holiday(ti)


# First we will run the tests using the default nighttime (sunset)
def test_get_rest_holiday():
    assert holiday.get_rest_holiday() is None


def test_get_work_holiday():
    assert holiday.get_work_holiday() is None


def test_is_holiday():
    assert hebcal.calendar.is_holiday(ti) is False


def test_is_rest_holiday():
    assert hebcal.calendar.is_rest_holiday(ti) is False


def test_is_shabbos():
    assert hebcal.calendar.is_shabbos(ti) is False


def test_is_rest_day():
    assert hebcal.calendar.is_rest_day(ti) is False
