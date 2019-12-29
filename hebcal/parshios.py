import pyluach
from pyluach import parshios


american_ashkinazik_parshios = [
            'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
            'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
            'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
            'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
            'Pekudei', 'Vayikra', 'Tzav', 'Shemini', 'Tazria', 'Metzora',
            'Acharei Mos', 'Kedoshim', 'Emor', 'Behar', 'Bechukosai',
            'Bamidbar', 'Naso', "Beha'aloscha", "Shelach", 'Korach', 'Chukas',
            'Balak', 'Pinchas', 'Matos', "Ma'sei", 'Devarim', "Va'eschanan",
            'Eikev', "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim',
            'Vayelech', 'Haazinu', "V'zos Habrocha"
            ]


class Parshios:
    def __init__(self, info):
        self.info = info

    def _pyluach_hebrew_date(self):
        return pyluach.dates.HebrewDate(self.info.hebrew_year(),
                                        self.info.hebrew_month(),
                                        self.info.hebrew_day())

    def _parsha_list(self):
        # Set the pronunciation
        # If an invalid pronunciation is provided, default to
        # "american_ashkinzik".
        if self.info.pronunciation == 'american_ashkinazik':
            return american_ashkinazik_parshios
        else:
            return american_ashkinazik_parshios

    def parsha(self):
        parsha_number = parshios.getparsha(self._pyluach_hebrew_date())
        if parsha_number is not None:
            return parsha_number[0]
        else:
            return None

    def parsha_string(self):
        return self._parsha_list()[self.parsha()]
