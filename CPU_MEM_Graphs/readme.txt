##ReadME###

About:
This scripts will generate graph for CPU and Memory Utilization of previous
date and email graphs

CPU graph contains CPU Idle, System and User values captured by SAR command
Memory graph contains Cache and Used memory values captured by SAR command

Pre-requisite:
Python 3.6
SAR
Pip to install (matplotlib>=3.1.1 and pandas>=0.25.0)
Bash/Shell
awk and sed
Server list in txt file
Password less login from execution server

Note: Make sure graph_cpu.py, graph_memory.py and sar_graph.sh should be in one directory

Syntax:

$sh sar_graph.sh servers.txt

Please change email address in 'sar_graph.sh' 

Last modify:
1. Modify graph name with server name and date ex. servername-01-Aug-2019-cpu.png
2. Added Server Name and Date in title of the graph
3. Added separate sar_csv.sh to generate csv report 
   Syntax: sh sar_csv.sh servers.txt 
