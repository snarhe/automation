import pandas as pd
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import dates as mpl_dates
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--server', help='Server IP/Hostname', required=True)
    parser.add_argument('-d','--rdate', help='Report date in format dd-MMM-YYYY', required=True)
    arguments = parser.parse_args()
    HOST = arguments.server
    RDATE = arguments.rdate
    return HOST, RDATE

HOST, RDATE = get_args()

plt.style.use('seaborn')

data = pd.read_csv('sar_mem.csv')
data['Time'] = pd.to_datetime(data['Time'],format= '%H:%M:%S' ).dt.time
#data['Time'] = [time.time() for time in data['Time']]
data.sort_values('Time', inplace=True)
Time = data['Time']
Used = data['Used']
Cache = data['Cache']

plt.plot_date(Time, Used, linestyle='solid', label='%used')
plt.plot_date(Time, Cache, linestyle='solid', label='%cache')
plt.gcf().autofmt_xdate()

plt.title('{} Memory Report: {}'.format(HOST, RDATE))
plt.xlabel('Server Time')
plt.ylabel('Memory Utilization in Percentage')
plt.legend()
plt.tight_layout()
plt.savefig('{}-{}-mem.png'.format(HOST, RDATE))

