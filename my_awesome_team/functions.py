from datetime import datetime as dt
import pytz
from django.conf import settings


def get_date_time(date, start=True):
    if start:
        date_time = dt.strptime(str(date) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    else:
        date_time = dt.strptime(str(date) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    timezone = pytz.timezone(settings.TIME_ZONE)
    return timezone.localize(date_time)

