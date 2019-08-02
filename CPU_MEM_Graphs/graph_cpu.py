import pandas as pd
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
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

data = pd.read_csv('sar_cpu.csv')
data['Time'] = pd.to_datetime(data['Time'],format= '%H:%M:%S' ).dt.time
#data['Time'] = [time.time() for time in data['Time']]
data.sort_values('Time', inplace=True)
Time = data['Time']
User = data['User']
System = data['System']
Idle = data['Idle']

plt.plot_date(Time, User, linestyle='solid', label='%user')
plt.plot_date(Time, System, linestyle='solid', label='%system')
plt.plot_date(Time, Idle, linestyle='solid', label='%idle')
plt.gcf().autofmt_xdate()

plt.title('{} CPU Report: {}'.format(HOST, RDATE))
plt.xlabel('Server Time')
plt.ylabel('CPU Utilization in Percentage')
plt.legend()
plt.tight_layout()
plt.savefig('{}-{}-cpu.png'.format(HOST, RDATE))

