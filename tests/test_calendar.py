from hebcal.calendar import Calendar
from hebcal import TimeInfo


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

ti = TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
              latitude=40.092383, longitude=-74.219996)

calendar = Calendar(ti)


# First we will run the tests using the default nighttime (sunset)
def test_get_rest_holiday():
    assert calendar.get_rest_holiday() is None


def test_get_work_holiday():
    assert calendar.get_work_holiday() is None


def test_is_holiday():
    assert Calendar.is_holiday(ti) is False


def test_is_rest_holiday():
    assert Calendar.is_rest_holiday(ti) is False


def test_is_shabbos():
    assert Calendar.is_shabbos(ti) is False
