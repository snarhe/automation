###########################################################################
#Name : pass_expire_alert.sh                                              #
#Version : 1.0                                                            #
#Description : Email alert for password expiry before 15 days             #
#              for each account on servers				  #
#Author : Sunil Narhe                                                     #
#Author Email : s.narhe@yahoo.in                                #
#URL :                                                                    #
#                                                                         #
#Requirement :                                                            #
#    1. Bash                                                              #
#    2. Python scripts days_till_date.py                                  #
#    3. Server IP addess in serverlist file                               #
#    4. Password less authentication to servers                           #
#       mentioned in serverlist file                                      #
#                                                                         #
#Usage : sh pass_expire_alert.sh                                          #
#                                                                         #
#Initial Draft : 14th Sep 2020                                            #
###########################################################################

#!/bin/bash
SCRIPT_PATH="/home/snarhe/suser_pass_expiry_alert"
PUSER="snarhe"

cd $SCRIPT_PATH

for Server in `cat $SCRIPT_PATH/input/serverlist`
do
    MIN_DAYS=`ssh $PUSER@$Server "grep '^UID_MIN' /etc/login.defs | sed 's/ /,/g' | rev | cut -d',' -f1 | rev"`
    MAX_DAYS=`ssh $PUSER@$Server "grep '^UID_MAX' /etc/login.defs | sed 's/ /,/g' | rev | cut -d',' -f1 | rev"`
    `ssh $PUSER@$Server "cat /etc/passwd > /tmp/passwd_$Server"`
    rsync $PUSER@$Server:/tmp/passwd_$Server $SCRIPT_PATH/tmp/
    awk -F':' -v "min=$MIN_DAYS" -v "max=$MAX_DAYS" '{ if ( $3 >= min && $3 <= max  && $7 != "/sbin/nologin" ) print $1 }' $SCRIPT_PATH/tmp/passwd_$Server > $SCRIPT_PATH/tmp/Users_$Server
    if [ -f $SCRIPT_PATH/report/report_$Server.csv ]
    then
        rm -rf "$SCRIPT_PATH/report/report_$Server.csv"
        rm -rf "$SCRIPT_PATH/html/html_part_$Server.html"
    fi
    for USERS in `cat $SCRIPT_PATH/tmp/Users_$Server`
    do
        EXPIRY_DATE=`ssh $PUSER@$Server "sudo chage -l $USERS | grep 'Password expires' | cut -d':' -f2 | grep -Ev 'never|password'"`
        if [ ! -z "$EXPIRY_DATE" ]
        then
            DAYS_TO_EXPIRE=`python $SCRIPT_PATH/python/days_till_date.py -ndt "$EXPIRY_DATE"`
            if [[ $DAYS_TO_EXPIRE -le 15 ]]
            then
                echo "$Server|$USERS|$EXPIRY_DATE" >> $SCRIPT_PATH/report/report_$Server.csv
                echo "<td>$Server</td><td>$USERS</td><td>$EXPIRY_DATE</td>" >> $SCRIPT_PATH/html/html_part_$Server.html
            fi
        fi
    done
done

for Server in `cat $SCRIPT_PATH/input/serverlist`
do
    `sed -i -e 's#^#<tr>#g' -e 's#$#</tr>#g' $SCRIPT_PATH/html/html_part_$Server.html`
    `sh $SCRIPT_PATH/shell/html_template.sh $SCRIPT_PATH/html/html_part_$Server.html`
    `python $SCRIPT_PATH/python/emessage.py`
done
