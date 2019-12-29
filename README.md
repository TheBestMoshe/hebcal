# Hebcal

### A python package for working with Hebrew dates, times, and holidays

#### Note: This is still in development and not ready for production. There will still be lots of breaking changes.

There are several python packages that deal with Hebrew dates, Z'manim and Jewish holidays. However, since the Hebrew calendar considers nightfall the beginning of the new day, I've found it very inconvenient to work with other packages. Just converting a Gregorian date to a Hebrew date doesn't give you the proper conversion, as it could be past nightfall, which needs to manually accommodated.

The same goes for any Jewish holiday package. You first need to figure out what the real Hebrew date is before you can determine if it's currently a holiday.

I wanted something that I can just ask "is today a rest holiday?" and I should get a True or False.

I wrote Hebcal to solve these problems. It takes in a latitude and longitude to calculate the location.
It can be installed through pip: `pip install hebcal`.

Here's a quick example:

```python
import hebcal

time_info = hebcal.TimeInfo.now(latitude=40.089909, longitude=-74.216270)
print(time_info.today_sunrise().strftime('%-I:%M:%S %p'))
###6:48:58 AM
print(time_info.hebrew_date())
###(5779, 7, 19)
```

You can input a specific date and time with a string:

```python
time_info = hebcal.TimeInfo('2018, 9, 27 10:07 pm', latitude=40.089909, longitude=-74.216270)
print(time_info.today_sunrise().strftime('%-I:%M:%S %p'))
###6:48:58 AM
print(time_info.hebrew_date())
###(5779, 7, 19)
```

The Hebrew date that is returned takes into account sunrise/sunset. If it's after sunset it will automatically return the correct Hebrew date.

You can also query directly if its night, or day

```python
print(time_info.is_night())
###True
print(time_info.is_day())
###False
```

<sub>
Note: Calculating the timezone from the lat/lon slows down the calculations. It is best to pass the timezone as an argument:</sub>

```python
time_info = hebcal.TimeInfo.now(timezone='America/New_York', latitude=40.089909, longitude=-74.216270)
```

You can manually get the timezone using Hebcal:

```python
from hebcal.util.location import get_location
timezone = get_location(latitude==40.089909, longitude=-74.216270)
print(timezone)
###America/New_York
```

### Hebcal zmanim.Zmanim

<sub>note: All times are datetime.datetime objects. They can be formated using `.strftime()`.</sub>

Here's an example of the hebcal.zmanim

```python
time_info = hebcal.TimeInfo.now(latitude=40.089909, longitude=-74.216270)

# pass a hbcal.TimeInfo object into Zmanim
zmanim = hebcal.Zmanim(time_info)
print(zmanim.last_shema_ma)
###2018-09-27 09:12:12.895624-04:00
print(zmanim.last_shema_ma.strftime("%-I:%M:%S %p"))
###9:12:12 AM
```

Other than accessing individual zmanim, You can just print the Zmanim object, which returns formated times (i.e. `9:12:12 AM`).

Another option is to get all the zmanim configures as json:

```python
zmanim_json = hebcal.Zmanim.json(time_info)
print(zmanim_json['earliest mincha'])
###2018-09-27 13:17:19.756457-04:00
```

Add calandar README here.
