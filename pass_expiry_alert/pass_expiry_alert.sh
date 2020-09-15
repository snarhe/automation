###########################################################################
#Name : pass_expire_alert.sh                                              #
#Version : 1.0                                                            #
#Description : Email alert for password expiry before 15 days             #
#Author : Sunil Narhe                                        			  #
#Author Email : s.narhe@yahoo.in										  #
#URL :									  								  #
#									 									  #
#Requirement :								  							  #
#    1. Bash								  							  #
#    2. Python scripts days_till_date.py				  				  #
#    3. Server IP addess in serverlist file				  				  #
#    4. Password less authentication to servers 			  			  #
#       mentioned in serverlist file					  				  #
#									  									  #
#Usage : sh pass_expire_alert.sh					   					  #
#									  									  #
#Initial Draft : 7th Sep 2020						  					  #
###########################################################################

#!/bin/bash
cd /home/snarhe/pass_expiry_alert
CURRENT_USER=`whoami`
for Server in `cat serverlist`
do
    EXPIRY_DATE=`ssh $CURRENT_USER@$Server "chage -l $CURRENT_USER | grep 'Password expires' | cut -d':' -f2"`
    DAYS_TO_EXPIRE=`python days_till_date.py -ndt "$EXPIRY_DATE"`
    if [ $DAYS_TO_EXPIRE -le 15 ]
    then
        `sh template.sh $Server "$EXPIRY_DATE"`
        `python emessage.py`
    fi
done
