from util import sun, proccess_time, location
import pyluach
from pyluach import dates
import datetime
from convertdate.hebrew import leap


class Date:
    def __init__(self, date_time, lat_lon, **kwargs):
        self.lat_lon = lat_lon

        if 'timezone' not in kwargs:
            print('timezone not in kwargs')
            self.timezone = location.get_timezone(self.lat_lon)
        else:
            self.timezone = kwargs['timezone']

        self.date_time = proccess_time.proccess_datetime(date_time,
                                                         timezone=self.timezone
                                                         )

        self.sun = sun.Sun(self.date_time, self.lat_lon,
                           timezone=self.timezone)

        if self.sun.is_yom():
            self.night = False
        else:
            self.night = True

        self.greg_year = int(self.date_time.strftime('%Y'))
        self.greg_month = int(self.date_time.strftime('%m'))
        self.greg_day = int(self.date_time.strftime('%d'))

        self.heb_date = dates.GregorianDate(self.greg_year,
                                            self.greg_month,
                                            self.greg_day
                                            ).to_heb(night=self.night)

        self.heb_year = self.heb_date.tuple()
        self.heb_month = self.heb_date.tuple()[1]
        self.heb_day = self.heb_date.tuple()[2]

    def month_title_english(self):
        titles = ['Nissan',
                  'Iyar',
                  'Sivan',
                  'Tamuz',
                  'Av',
                  'Elul',
                  'Tishrei',
                  'Cheshvon',
                  'Kislev',
                  'Teves',
                  'Shevat']
        if leap(self.heb_year):
            titles.append('Adar I')
            titles.append('Adar II')
        else:
            titles.append('Adar')

        return titles[self.heb_month - 1]

    def day_title_aleph_bet(self):
        titles = (' א ב ג ד ה ו ז ח ט י'
                  ' יא יב יג יד טו טז יז יח יט כ '
                  'כא כב כג כד כה כו כז כח כט ל ').split()
        return titles[self.heb_day - 1]


if __name__ == '__main__':
    d = Date('2018 9 18 8:00 pm', (40.092383, -74.219996),
             timezone='America/New_York')
    print(d.heb_date.to_greg())
    print(d.heb_day)
    print((d.heb_date + 1))
    print(d.month_title_english())
