import hebcal
from hebcal import parshios


ti = hebcal.TimeInfo(
    "2018, 9, 19, 7:15 pm",
    timezone="America/New_York",
    latitude=40.092383,
    longitude=-74.219996,
)

parshios = parshios.Parshios(ti)


def test_parsha_string():
    assert parshios.parsha_string() == "Haazinu"


def test_pyluach_hebrew_date():
    assert str(parshios._pyluach_hebrew_date()) == "5779-7-11"


def test_parsha():
    assert parshios.parsha() == 52


def test_parsha_list():
    assert parshios._parsha_list() == hebcal.parshios.american_ashkinazik_parshios
