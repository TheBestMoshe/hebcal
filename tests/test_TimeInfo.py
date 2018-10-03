from hebcal import TimeInfo

ti = TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
              latitude=40.092383, longitude=-74.219996)


def test_today_sunset():
    assert str(ti.today_sunset()) == '2018-09-19 18:59:12.782791-04:00'


def test_today_sunrise():
    assert str(ti.today_sunrise()) == '2018-09-19 06:41:18.851418-04:00'


def test_is_day():
    assert ti.is_day() is False


def test_is_night():
    assert ti.is_night() is True


def test_hebrew_date():
    assert str(ti.hebrew_date()) == '(5779, 7, 11)'


def test_alternate_hebrew_date():
    from hebcal import zmanim

    zmanim = zmanim.Zmanim(ti)
    ti.alternate_nighttime = zmanim.night_72
    assert str(ti.alternate_hebrew_date()) == '(5779, 7, 10)'
    assert ti.hebrew_day() == 11


def test_is_next_hebrew_day():
    assert ti.is_next_hebrew_day() is True


def test_today_dawn():
    assert str(ti.today_dawn()) == '2018-09-19 05:20:28.556570-04:00'


def test_today_dusk():
    assert str(ti.today_dusk()) == '2018-09-19 17:30:13.696051-04:00'

# print(ti.today_dawn())