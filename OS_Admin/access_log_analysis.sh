#!/bin/bash
# ######################################################################################################################
# ----------------------------------------------------------------------------------------------------------------------
# Date of last commit:      $Date: 2022-05-16 10:21 +0530
# ----------------------------------------------------------------------------------------------------------------------
#      Author: 
#
#      PURPOSE: 
#
#
######################################################################################################################

#Variables
DATE=$(date +'%d_%b_%Y_%M_%H_%S')
BASEPATH=`pwd`
LOGDIR=$BASEPATH/logs
LOGFILE=$LOGDIR/access_log_analysis_$DATE.log
REPORT_LOG=$LOGDIR/access_log_analysis_$DATE.csv

#Read the content provided by user
IndexOf()    {
    local i=1 S=$1; shift
    while [ $S != $1 ]
    do    ((i++)); shift
        [ -z "$1" ] && { i=0; break; }
    done
    echo "`expr $i + 1`"
}

#Creating log file
LOGIT()
{
    local message=$1
    local timestamp=$(date +'%d %b %Y %T')
    #echo "[${timestamp}]        $message"
    echo "[${timestamp}]        $message" >> $LOGFILE
}

#Extracting Log directory
#Checking type and which commands are installed or not
#so we can find path of unzip command to extract
EXTRACT_LOG()
{
    local log_file_name=$1
    LOGIT "INFO    Checking required packages to unzip logfile"
    if [[ `type type > /dev/null ; echo $?` == 0 ]]
    then
        type_status=1
    else
        type_status=0
    fi
    if [[ `which which > /dev/null ; echo $?` == 0 ]]
    then 
        which_status=1
    else
        which_status=0
    fi
    if [[ $type_status == 1 ]]
    then
        LOGIT "INFO    TYPE module found"
        UNZIP_PATH=`type unzip | awk '{print $NF}'`
    elif [[ $which_status == 1 ]]
    then
        LOGIT "INFO    WHICH module found"
        UNZIP_PATH=`which unzip`
    else
        LOGIT "ERROR    No TYPE/WHICH module found, install it manually"
        exit 0
    fi
    LOGIT "INFO    Extracting log file"
    $UNZIP_PATH -qq $log_file_name 
    LOGIT "INFO    Extract completed"
}

#Main body of script
#Creating log directory in BASEPATH/'pwd'
mkdir -p $LOGDIR
if [[ -f $BASEPATH/serv_acc.zip ]]
then
    EXTRACT_LOG $BASEPATH/serv_acc.zip
    #Coping all .csv files to tmp file to convert in array
    ls -l $BASEPATH/serv_acc/*.csv | awk -F'/' '{print $NF}' > $LOGDIR/log_file_list.txt
    if [[ -f $LOGDIR/log_file_list.txt ]]
    then
        #Creating log file array
        log_file_list_array=($(cat $LOGDIR/log_file_list.txt | sed 's#\n#,#g'))
        LOGIT "INFO    Getting log file details"
        echo "The logs array contains ${#log_file_list_array[@]} files"
        #Print Menu to accept file name by its number
        for i in "${!log_file_list_array[@]}"
        do
            echo "    `expr $i + 1`    ${log_file_list_array[$i]}"
        done
        LOGIT "INFO    Accepting Log file name from User"
        #Reading file name from array [Menu]
        read -p "Enter the number of the file in the menu above you wish to search, i.e. [1,2,3,4 or 5] " log_file_name
        echo "You have selected $log_file_name"
        LOGIT "INFO    We will process file ${log_file_list_array[`expr $log_file_name - 1`]}"
        LOGIT "INFO    Accepting field parameter to search"
        #Printing operation menu 
        echo ""
        echo "Select search filed one or many:"
        echo "    PROTOCOL='TCP/UDP/ICMP/GRE'"
        echo "    SRCIP=<SOURCE IP>"
        echo "    SRCPORT=<SOURCE PORT>"
        echo "    DSTIP=<DESTINATION IP>"
        echo "    DSTPORT=<DESTINATION PORT>"
        echo "    PACKETS <CRITERIA> <SIZE>"
        echo "    BYTES <CRITERIA> <SIZE>"
        echo ""
        read -p "    " search_field
        echo "Search Field: $search_field"
        #Checking operating provided by user and functioning
        if [[ `echo $search_field | grep PROTOCOL > /dev/null;echo $?` == 0 ]]
        then
            #Getting the index of operation
            check_pattern_index=`IndexOf 'PROTOCOL' ${search_field[@]}`
            field_index=`expr $check_pattern_index + 1`
            check_pattern_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            #echo "Value of PROTOCOL: $check_pattern_value"
            #Performing search on data file and printing it on terminal
            awk -F',' -v protocol="$check_pattern_value" '$3 ~ protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
        elif [[ `echo $search_field | grep SRCIP > /dev/null;echo $?` == 0 ]]
        then
            check_srcip_index=`IndexOf 'SRCIP' ${search_field[@]}`
            field_index=`expr $check_srcip_index + 1`
            check_srcip_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            echo "Value of SRCIP: $check_srcip_value"
            awk -F',' -v protocol="$check_srcip_value" '$4 ~ protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
        elif [[ `echo $search_field | grep SRCPORT > /dev/null;echo $?` == 0 ]]
        then
            check_srcport_index=`IndexOf 'SRCPORT' ${search_field[@]}`
            field_index=`expr $check_srcport_index + 1`
            check_srcport_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            echo "Value of SRCIP: $check_srcport_value"
            awk -F',' -v protocol="$check_srcport_value" '$5 ~ protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
        elif [[ `echo $search_field | grep DSTIP > /dev/null;echo $?` == 0 ]]
        then
            check_dstip_index=`IndexOf 'DSTIP' ${search_field[@]}`
            field_index=`expr $check_dstip_index + 1`
            check_dstip_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            echo "Value of DSTIP: $check_dstip_value"
            awk -F',' -v protocol="$check_dstip_value" '$6 ~ protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
        elif [[ `echo $search_field | grep DSTPORT > /dev/null;echo $?` == 0 ]]
        then
            check_dstport_index=`IndexOf 'DSTPORT' ${search_field[@]}`
            field_index=`expr $check_dstport_index + 1`
            check_dstport_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            echo "Value of DSTIP: $check_dstport_value"
            awk -F',' -v protocol="$check_dstport_value" '$7 ~ protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
        elif [[ `echo $search_field | grep PACKETS > /dev/null;echo $?` == 0 ]]
        then
            check_packet_index=`IndexOf 'PACKETS' ${search_field[@]}`
            #Getting Operator like <,>,=,!=
            operator_index=`expr $check_packet_index + 1`
            check_opt_value=`echo $search_field | cut -d"=" -f$operator_index | sed "s/'//g"`
            field_index=`expr $check_packet_index + 2`
            check_packet_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            awk -F',' -v protocol="$check_packet_value" -v operator="$check_opt_value" '$8 operator protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
            #Getting some of all searched packets
            Total_Packets=`cat $REPORT_LOG | awk -F',' '{ sum+=$8 } END {print sum}'`
            echo "Total Packets : $Total_Packets"
        elif [[ `echo $search_field | grep BYTES > /dev/null;echo $?` == 0 ]]
        then
            check_bytes_index=`IndexOf 'BYTES' ${search_field[@]}`
            operator_index=`expr $check_bytes_index + 1`
            check_opt_value=`echo $search_field | cut -d"=" -f$operator_index | sed "s/'//g"`
            field_index=`expr $check_bytes_index + 2`
            check_bytes_value=`echo $search_field | cut -d"=" -f$field_index | sed "s/'//g"`
            echo "Value of DSTIP: $check_dstport_value Operator: $check_opt_value"
            awk -F',' -v protocol="$check_dstport_value" -v operator="$check_opt_value" '$9 operator protocol' $BASEPATH/serv_acc/${log_file_list_array[`expr $log_file_name - 1`]} > $REPORT_LOG
            echo ""
            cat $REPORT_LOG
            echo ""
            #Getting some of all searched bytes
            Total_Bytes=`cat $REPORT_LOG | awk -F',' '{ sum+=$9 } END {print sum}'`
            echo "Total Bytes : $Total_Bytes"
        fi
    else
        LOGIT "ERROR    Empty log directory"
        exit 0
    fi
    #Removing the unzip file
    rm -rf $BASEPATH/serv_acc
else
    LOGIT "ERROR    Please copy serv_acc.zip file in $BASEPATH"
fi
