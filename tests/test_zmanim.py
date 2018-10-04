import pytest
import hebcal


ti = hebcal.TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
                     latitude=40.092383, longitude=-74.219996)
zmanim = hebcal.Zmanim(ti)


def test_alot_hashachar():
    assert str(zmanim.alot_hashachar()) == '2018-09-19 05:20:28.556570-04:00'


def test_last_shema_ma():
    assert str(zmanim.last_shema_ma()) == '2018-09-19 09:09:47.334261-04:00'


def test_last_tefila_gra():
    assert str(zmanim.last_tefila_gra()) == '2018-09-19 10:47:16.828542-04:00'


def test_plag_hamincha():
    assert str(zmanim.plag_hamincha()) == '2018-09-19 17:42:20.914940-04:00'


def test_night_72():
    assert str(zmanim.night_72()) == '2018-09-19 20:11:12.782791-04:00'
