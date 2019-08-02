#!/bin/bash

FN=$1
EMAIL='s.narhe@yahoo.in'
SAR_DATE=`date -d "1 day ago" +%d`
Y_DATE=`date -d '1 day ago' +%d-%b-%Y`

for SERVER in `cat $FN`
do
    ssh $SERVER -q "LC_TIME=en_UK.utf8 sar -r -f /var/log/sa/sa$SAR_DATE -s 00:00:00 -e 23:00:00 | egrep -v '(Linux|Average|memused)'" | sed '/^$/d'> sar_mem_raw.csv
    ssh $SERVER -q "LC_TIME=en_UK.utf8 sar -f /var/log/sa/sa$SAR_DATE -s 00:00:00 -e 23:00:00 | egrep -v '(Linux|Average|idle)'" | sed '/^$/d' > sar_cpu_raw.csv
    awk '{print $1","$2","$3","$4","$5","$6","$7","$8; }' sar_cpu_raw.csv > $SERVER-$Y_DATE-sar_cpu.csv
    awk '{print $1","$2","$3","$4","$5","$6","$7","$8; }' sar_mem_raw.csv > $SERVER-$Y_DATE-sar_mem.csv
    sed -i '1i Time,CPU,PercentUser,PercentNice,PercentSystem,IOWait,Steal,Idle' $SERVER-$Y_DATE-sar_cpu.csv
    sed -i '1i Time,kbmemfree,kbmemused,percentmemused,kbbuffers,kbcached,kbcommit,PercentCommit' $SERVER-$Y_DATE-sar_mem.csv
    echo -e "Hello,\n\nPlease find attached sar report for date $Y_DATE.\n\n\nRegards,\nSunil N" | mail -s "$SERVER SAR Report $Y_DATE" -a $SERVER-$Y_DATE-sar_cpu.csv -a $SERVER-$Y_DATE-sar_mem.csv $EMAIL
    rm -rf $SERVER-$Y_DATE-sar_mem.csv $SERVER-$Y_DATE-sar_cpu.csv sar_cpu_raw.csv sar_mem_raw.csv
done