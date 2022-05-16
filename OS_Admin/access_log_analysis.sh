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

ANALYSIS_LOG()
{
    local message=$1
    local timestamp=$(date +'%d %b %Y %T')
    echo "$message"
    echo "$message" >> $REPORT_LOG
}

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
mkdir -p $LOGDIR
if [[ -f $BASEPATH/serv_acc.zip ]]
then
    EXTRACT_LOG $BASEPATH/serv_acc.zip
    ls -l $BASEPATH/serv_acc/*.csv | awk -F'/' '{print $NF}' > $LOGDIR/log_file_list.txt
    if [[ -f $LOGDIR/log_file_list.txt ]]
    then
        log_file_list_array=($(cat $LOGDIR/log_file_list.txt | sed 's#\n#,#g'))
        LOGIT "INFO    Getting log file details"
        echo "The logs array contains ${#log_file_list_array[@]} files"
        for i in "${!log_file_list_array[@]}"
        do
            echo "    `expr $i + 1`    ${log_file_list_array[$i]}"
        done
        LOGIT "INFO    Accepting Log file name from User"
        read -p "Enter the number of the file in the menu above you wish to search, i.e. [1,2,3,4 or 5] " log_file_name
        echo "You have selected $log_file_name"
        LOGIT "INFO    We will process file ${log_file_list_array[`expr $log_file_name - 1`]}"
        LOGIT "INFO    Accepting field parameter to search"
        echo "    "
    else
        LOGIT "ERROR    Empty log directory"
        exit 0
    fi
    
else
    LOGIT "ERROR    Please copy serv_acc.zip file in $BASEPATH"
fi

