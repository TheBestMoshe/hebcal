from datetime import timedelta, datetime


class Zmanim:
    def __init__(self, info):
        self.info = info

    def __repr__(self):
        return f'hebcal.zmanim.Zmanim({self.info})'

    def sunrise(self):
        """ Returns the time of sunrise """
        return self.info.today_sunrise()

    def sunset(self):
        """ Returns the time of sunset """
        return self.info.today_sunset()

    def alot_hashachar(self):
        """Return the time for Alot Hashachar

        Alot Hashachar is dawn. This is calculated when the sun is 16.1°
        below the eastern geometric horizon before sunrise (-16.1°).
        This calculation is based on the same calculation of 72 minutes but
        uses a degree based calculation instead of 72 exact minutes. This
        calculation is based on the position of the sun 72 minutes before
        sunrise in Jerusalem during the equinox, which calculates to 16.1°
        below geometric zenith.

        For more information see https://www.myzmanim.com/read/degrees.aspx

        """
        return self.info.today_dawn()

    # Tzait_hakovhavim needs to be added

    def alot_72(self):
        """Return the time for Alot calculated with 72 minutes before sunrise 
        """

        return self.sunrise() - timedelta(minutes=72)

    def night_72(self):
        """ Return thetime for nightfall, 72 minutes after sunset """
        return self.sunset() + timedelta(minutes=72)

    def sun_hours(self):
        """ Return one Shah Zmanios in seconds

        This is calculated by deviding the time between sunrise and sunset by
        12. This is the opinion of the Gra.
        """
        return (self.sunset().timestamp() - self.sunrise().timestamp()) / 12

    def sun_hours_ma(self):
        """ Return on Shah Zmanios in seconds, according to the Magen Avrahom

        This Shaos Zmanios is based on the opinion of the Magen Avrahom, that
        it is calculated from Alot to nightfall.
        The time is calculated by deviding Alot_72 and Night_72 by 12.

        """
        return (self.night_72().timestamp() - self.alot_72().timestamp()) / 12

    def last_shema_gra(self):
        """ Return the last Shema using Shaos Zmanios of the Gra """
        return self.sunrise() + timedelta(seconds=(self.sun_hours() * 3))

    def last_shema_ma(self):
        """ Return the last Shema using Shaos Zmanios of the Magen Avrahom """
        return self.alot_72() + timedelta(seconds=(self.sun_hours_ma() * 3))

    def last_tefila_gra(self):
        """ Return Sof Zman Tefila using Shaos Zmanios of the Gra """
        return self.sunrise() + timedelta(seconds=(self.sun_hours() * 4))

    def last_tefila_ma(self):
        """ Return Sof Zman Tefila using Shaos Zmanios of the Magen Avrahom """
        return self.alot_72() + timedelta(seconds=(self.sun_hours_ma() * 4))

    def midday(self):
        """ Return the time for midday (chatzot) 

        This is calculated using Shaos Zmanios according to the Gra
        """
        return self.sunrise() + timedelta(seconds=(self.sun_hours() * 6))

    def mincha_gedola(self):
        """ Return the time for Mincha Gedola

        This is calculated using Shaos Zmanios according to the Gra
        """
        return self.sunrise() + timedelta(seconds=(self.sun_hours() * 9.5))

    # Need to add Mincha Ketana

    def plag_hamincha(self):
        """ Return the time for Plag Hamincha

        This is calculated using Shaos Zmanios according to the Gra
        """
        return self.sunrise() + timedelta(seconds=(self.sun_hours() * 10.75))

    def time_passed(self, item):
        """Check if a specific zman has passed

        Pass in a hebcal.Zmanim object to check if the time has allready passed

        Args:
            item (obj): datetime object. It should be a Zmanim object

        Returns:
            bool: True if zman has passed. Otherwise, False
        """

        if item.timestamp() < datetime.now().timestamp():
            return True
        else:
            return False

    def next_zman(self):
        """ Returns the upcoming zman

        Note: This method should only be used if TimeInfo is set to the current
        time.
        """
        zmanim = self.json()
        for zman in zmanim:
            if not self.time_passed(zmanim[zman]):
                return zman, zmanim[zman]

        # If all the zmanim of this day have passed, return Alot for the next
        # day.
        return 'alot', self.info.next_dawn

    def json(self):
        zmanim = {'alot': self.alot_hashachar(),
                  'sunrise': self.sunrise(),
                  'last shema ma': self.last_shema_ma(),
                  'last shema gra': self.last_shema_gra(),
                  'last shachris ma': self.last_tefila_ma(),
                  'last shachris gra': self.last_shema_gra(),
                  'midday': self.midday(),
                  'mincha gedola': self.mincha_gedola(),
                  'plag hamincha': self.plag_hamincha(),
                  'sunset': self.sunset(),
                  'nightfall 72': self.night_72(),
                  }
        return zmanim

    def __str__(self):
        return (f'Alot (16.1 degrees): {self.alot_hashachar().strftime("%-I:%M:%S %p")}\n'
                f'Sunrise: {self.sunrise().strftime("%-I:%M:%S %p")}\n'
                f'Last Shema MA: {self.last_shema_ma().strftime("%-I:%M:%S %p")}\n'
                f'Last Shema Gra: {self.last_shema_gra().strftime("%-I:%M:%S %p")}\n'
                f'Last Shachris MA: {self.last_tefila_ma().strftime("%-I:%M:%S %p")}\n'
                f'Last Shachris Gra: {self.last_tefila_gra().strftime("%-I:%M:%S %p")}\n'
                f'Midday: {self.midday().strftime("%-I:%M:%S %p")}\n'
                f'Mincha Gedola: {self.mincha_gedola().strftime("%-I:%M:%S %p")}\n'
                f'Plag Hamincha: {self.plag_hamincha().strftime("%-I:%M:%S %p")}\n'
                f'Sunset: {self.sunset().strftime("%-I:%M:%S %p")}\n'
                f'72: {self.night_72().strftime("%-I:%M:%S %p")}\n'
                )
