"""
Name : graph_memory.py
Version : 1.0
Description : Monitor Linux servers CPU, Memory, Disk, Yum Logs and Failed Logins
Author : Sunil Narhe
Author Email : s.narhe@yahoo.in
URL :

Requirement :
    1. Python 3.6
    2. pip 3
    3. pandas matplotlib numpy

Usage : python monitoring.py -f server_list.txt

Sub script: graph_memory.py (To generate graph images for Memory
"""

import pandas as pd
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from matplotlib import dates as mpl_dates
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ifile','--inputfile', help='Input file name with path if any', required=True)
    parser.add_argument('-p','--purpose', help='Purpose of grapgh Used/Free', required=True)
    arguments = parser.parse_args()
    INPUTFILE = arguments.inputfile
    PURPOSE = arguments.purpose
    return INPUTFILE, PURPOSE

INPUTFILE, PURPOSE = get_args()

plt.style.use('ggplot')

data = pd.read_csv(INPUTFILE)
data.sort_values('HostName', inplace=True)
HostName = data['HostName']
Memory = data['Memory']

y_pos = np.arange(len(HostName))

plt.xlabel('Hosts')
if PURPOSE == "free":
    plt.title('Free Memory Report')
    plt.ylabel('Utilization in Percentage')
    plt.bar(y_pos/2., Memory, align='center', alpha=0.5, width=0.1, color="#006D2C")
elif PURPOSE == "used":
    plt.title('Used Memory Report')
    plt.ylabel('Utilization in Percentage')
    plt.bar(y_pos/2., Memory, align='center', alpha=0.5, width=0.1, color="#FF5733")
plt.xticks(y_pos/2., HostName, rotation=90)
plt.tight_layout()
plt.savefig('{}_mem.png'.format(PURPOSE))
