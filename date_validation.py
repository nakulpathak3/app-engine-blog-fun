months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):
    cap_month = month.capitalize()
    if cap_month in months:
        return month.capitalize()
    return None

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
    if year > 1900 and year < 2020:
            return year

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day >= 1 and day <= 31:
            return int(day)