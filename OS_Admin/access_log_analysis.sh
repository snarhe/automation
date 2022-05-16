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

#Print Help menu
HELP()
{
echo "    --server: Server IP/Hostname (Which Access log file given name)";
echo "    --protocol <protocol>: Protocol which you want search like TCP,UDP";
echo "    --logfile <file_name>: Log File name";
echo "    --srcip <IP/HOST> Source IP/Hostname used in Access log to captured";
echo "    --dstip <IP/HOST> Destination IP/Hostname used in Access log to captured";
echo "    --pktsize: Packet size must with greater than (-gt), less than (-lt), equal to (-eq) or not equal to !(eq)";
echo "    --help: To print this help menu";
echo ""
}

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
    echo "[${timestamp}]        $message"
    echo "[${timestamp}]        $message" >> $LOGFILE
}

ANALYSIS_LOG()
{
    local message=$1
    local timestamp=$(date +'%d %b %Y %T')
    echo "$message"
    echo "$message" >> $REPORT_LOG
}


#Main body of script
mkdir -p $LOGDIR
if [[ $# == 0 ]]
then
    LOGIT "Error    At least one parameter is manadatory. Use 'sh $0 --help'";
elif [ $1 == '--help' ]
then
    HELP
else
    parameter_list=$@
    if [[ `echo $parameter_list | grep -e '--server' > /dev/null; echo $?` == 0 ]]
    then
        server_index="`IndexOf '--server' ${parameter_list[@]}`"
        server_values=`echo $parameter_list | cut -d" " -f$server_index`
        LOGIT "INFO    Checking Access Log file"
        ACCESS_LOG_FILE_NAME=$BASEPATH/$server_values.zip
        if [[ -f $ACCESS_LOG_FILE_NAME ]]
        then
            LOGIT "INFO    Access Log file found ($ACCESS_LOG_FILE_NAME)"
            LOGIT "INFO    Checking required parameter"
            if [[ `echo $parameter_list | grep -e '--protocol' > /dev/null; echo $?` == 0 ]]
            then
                PROTOCOL_LOGS
            elif [[ `echo $parameter_list | grep -e '--logfile' > /dev/null; echo $?` == 0 ]]
            then
                REPORT_LOG_FILE
            elif [[ `echo $parameter_list | grep -e '--srcip' > /dev/null; echo $?` == 0 ]]
            then
                SRCIP
            elif [[ `echo $parameter_list | grep -e '--dstip' > /dev/null; echo $?` == 0 ]]
            then
                DSTIP
            elif [[ `echo $parameter_list | grep -e '--pktsize' > /dev/null; echo $?` == 0 ]]
            then
                PKTSIZE
            fi
        else
            LOGIT "ERROR    Access log file not found on server"
            exit 0
        fi
    else
        LOGIT "Error    --server parameter is manadatory."
        exit 0
    fi
fi
