"""
Name : days_till_date.py
Version : 1.0
Description : Print number of days till date given
Author : Sunil Narhe
Author Email : s.narhe@yahoo.in
URL :

Requirement :
    1. Python 3.6
    2. pip 3
    3. paramiko, smtplib

Usage : python days_till_date.py -ndt 'Dec 15, 2020' 

"""

#!/usr/bin/python
from datetime import datetime
from datetime import date
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ndt','--nextdate', help='Next date to calculate days from now', required=True)
    arguments = parser.parse_args()
    NEXTDATE = arguments.nextdate
    return NEXTDATE

NEXTDATE = get_args()

date_dt1 = datetime.strptime(NEXTDATE.strip(), '%b %d, %Y').date()
date_expire = int(date_dt1.strftime('%d'))
month_expire = int(date_dt1.strftime('%m'))
year_expire = int(date_dt1.strftime('%Y'))

today = date.today()
date_today = int(today.day)
month_today = int(today.month)
year_today = int(today.year)

d0 = date(year_expire, month_expire, date_expire)
d1 = date(year_today,month_today,date_today)
delta =  d0 - d1
print(delta.days)

