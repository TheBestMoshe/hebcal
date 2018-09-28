import pytest
from hebcal import util


@pytest.mark.skip(reason='This slows down the test')
def test_get_timezone():
    assert util.location.get_timezone(40.092383, -74.219996) == 'America/New_York'


def test_proccess_datetime():
    assert str(util.proccess_time.proccess_datetime('2018, 9, 19, 7:15 pm')) == '2018-09-19 19:15:00'


def test_proccess_datetime_with_timezone():
    assert str(util.proccess_time.proccess_datetime('2018, 9, 19, 7:15 pm',
                                                    timezone='America/New_York'
                                                    )) == '2018-09-19 19:15:00-04:00'


print(util.proccess_time.proccess_datetime('2018, 9, 19, 7:15 pm', timezone='America/New_York'))