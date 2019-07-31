#!/bin/bash

FN=$1

SAR_DATE=`date -d "1 day ago" +%d`
Y_DATE=`date -d '1 day ago' +%d-%b-%Y`

for SERVER in `cat $FN`
do
    MEM=`ssh $SERVER -q "free | grep Mem"`
    TOTAL_MEM=`echo $MEM | awk '{print $2}'`
    #echo "System Memory $SERVER $TOTAL_MEM"
    ssh $SERVER -q "LC_TIME=en_UK.utf8 sar -r -f /var/log/sa/sa$SAR_DATE -s 00:00:00 -e 23:00:00 | egrep -v '(Linux|Average|memused)'" | sed '/^$/d'> sar_mem_raw.csv
    ssh $SERVER -q "LC_TIME=en_UK.utf8 sar -f /var/log/sa/sa29 -s 00:00:00 -e 23:00:00 | egrep -v '(Linux|Average|idle)'" | sed '/^$/d' > sar_cpu_raw.csv
        sed -i "s/$/\t$TOTAL_MEM/g" sar_mem_raw.csv
        #tail -5 sar_mem_raw.csv
        awk '$10=100*$6/$9 {print $1,$4,$10}' sar_mem_raw.csv > sar_mem_raw1.csv
        awk '{print $1","$2","$3; }' sar_mem_raw1.csv > sar_mem.csv
        awk '{print $1","$3","$5","$8; }' sar_cpu_raw.csv > sar_cpu.csv
        sed -i '1i Time,User,System,Idle' sar_cpu.csv
        sed -i '1i Time,Used,Cache' sar_mem.csv
        python graph_cpu.py &> /dev/null
        python graph_memory.py &> /dev/null
        echo -e "Hello,\n\nPlease find attached sar report for date $Y_DATE.\n\n\nRegards,\nSunil N" | mail -s "$SERVER SAR Report $Y_DATE" -a cpu.png -a mem.png sunil.narhe@capgemini.com
        rm -rf cpu.png mem.png sar_mem_raw.csv sar_cpu_raw.csv sar_mem_raw1.csv sar_mem.csv sar_cpu.csv
done
