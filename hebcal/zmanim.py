from datetime import timedelta


class Zmanim:
    def __init__(self, info):
        self.sunrise = info.today_sunrise()
        self.sunset = info.today_sunset()
        self.alot_hashachar = info.today_dawn()
        self.tzait_hakochavim = info.today_dusk()
        
        self.alot_72 = self.sunrise - timedelta(minutes=72)
        self.night_72 = self.sunset + timedelta(minutes=72)

        self.sun_hours = (self.sunset.timestamp() -
                          self.sunrise.timestamp()) / 12
        self.sun_hours_ma = (self.night_72.timestamp() -
                             self.alot_72.timestamp()) / 12

        self.last_shema_gra = self.sunrise + timedelta(seconds=(self.sun_hours * 3))
        self.last_shema_ma = self.alot_72 + timedelta(seconds=(self.sun_hours_ma * 3))

        self.last_tefila_gra = self.sunrise + timedelta(seconds=(self.sun_hours * 4))
        self.last_tefila_ma = self.alot_72 + timedelta(seconds=(self.sun_hours_ma * 4))

        self.midday = self.sunrise + timedelta(seconds=(self.sun_hours * 6))

        self.big_mincha = self.sunrise + timedelta(seconds=(self.sun_hours * 6.5))
        
        # Need to add Mincha Ketana

        self.plag_hamincha = self.sunrise + timedelta(seconds=(self.sun_hours * 10.75))
    
    @classmethod
    def json(cls, info):
        z = Zmanim(info)
        zmanim = {'alot': z.alot_hashachar,
                  'sunrise': z.sunrise,
                  'last shema ma': z.last_shema_ma,
                  'last shema gra': z.last_shema_gra,
                  'last shachris ma': z.last_tefila_ma,
                  'last shachris gra': z.last_shema_gra,
                  'midday': z.midday,
                  'earliest mincha': z.big_mincha,
                  'plag hamincha': z.plag_hamincha,
                  'sunset': z.sunset,
                  'nightfall 72': z.night_72,
                  }
        return zmanim

    def __str__(self):
        return (f'Alot (16.1 degrees): {self.alot_hashachar.strftime("%-I:%M:%S %p")}\n'
                f'Sunrise: {self.sunrise.strftime("%-I:%M:%S %p")}\n'
                f'Last Shema MA: {self.last_shema_ma.strftime("%-I:%M:%S %p")}\n'
                f'Last Shema Gra: {self.last_shema_gra.strftime("%-I:%M:%S %p")}\n'
                f'Last Shachris MA: {self.last_tefila_ma.strftime("%-I:%M:%S %p")}\n'
                f'Last Shachris Gra: {self.last_tefila_gra.strftime("%-I:%M:%S %p")}\n'
                f'Midday: {self.midday.strftime("%-I:%M:%S %p")}\n'
                f'Earliest Mincha: {self.big_mincha.strftime("%-I:%M:%S %p")}\n'
                f'Plag Hamincha: {self.plag_hamincha.strftime("%-I:%M:%S %p")}\n'
                f'Sunset: {self.sunset.strftime("%-I:%M:%S %p")}\n'
                f'72: {self.night_72.strftime("%-I:%M:%S %p")}\n'
                )


if __name__ == '__main__':
    from __init__ import TimeInfo

    # ti = TimeInfo.now(timezone='America/New_York',
    #                   latitude=40.092383, longitude=-74.219996)
    ti = TimeInfo('2018, 9, 19, 7:15 pm', timezone='America/New_York',
                  latitude=40.092383, longitude=-74.219996)
    
    z = Zmanim.json(ti)
    # print(z.sun_hours)
    # print(z.last_shema_gra.strftime('%-I:%M:%S %p'))
    # print(z.last_shema_ma.strftime('%-I:%M:%S %p'))
    # print(z.alot_hashachar.strftime('%-I:%M:%S %p'))
    # print(z.alot_72.strftime('%-I:%M:%S %p'))
    # print(z.tzait_hakochavim.strftime('%-I:%M:%S %p'))
    # print(f"Midday: {z.midday.strftime('%-I:%M:%S %p')}")
    # print(f"Mincha Gedola: {z.big_mincha.strftime('%-I:%M:%S %p')}")
    # print(f"Plag: {z.plag_hamincha.strftime('%-I:%M:%S %p')}")
    for item in z:
        print(item + ': ' + z[item].strftime("%-I:%M:%S %p"))