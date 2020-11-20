#!/usr/local/bin/python2.7
"""
Name : pcap_summay.py
Version : 1.0
Description : Read PCAP file and print summary
Author : Sunil Narhe
Author Email : virtumentor@gmail.com
URL :
Requirement :
    1. Python 2.7
    2. pip 2
    3. dpkt

Usage : python pcap_summary.py -f test1.pcap

"""

import dpkt
import argparse
import datetime
import socket

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--pcap', help='PCAP file name', required=True)
    arguments = parser.parse_args()
    InputFile = arguments.pcap
    return InputFile

InputFile = get_args()

def pcap_summary():
    counter=0
    ipcounter=0
    tcpcounter=0
    udpcounter=0
    for ts, pkt in dpkt.pcap.Reader(open(InputFile,'r')):
        counter+=1
        eth=dpkt.ethernet.Ethernet(pkt) 
        if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
           continue
        ip=eth.data
        ipcounter+=1
        if ip.p==dpkt.ip.IP_PROTO_TCP: 
           tcpcounter+=1
        if ip.p==dpkt.ip.IP_PROTO_UDP:
           udpcounter+=1
    print "------------------- SUMMARY START ---------------"
    print "Total number of packets in the pcap file: ", counter
    print "Total number of ip packets: ", ipcounter
    print "Total number of tcp packets: ", tcpcounter
    print "Total number of udp packets: ", udpcounter
    print "------------------- SUMMARY END -----------------"

def print_packet_info(ts, src_ip, src_port, dst_ip, dst_port, protocol, pkt_len, ttl):
    utc_timestamp = str(datetime.datetime.utcfromtimestamp(ts))
    log_line = '[%s] - %s:%s -> %s:%s (%s, len=%d, ttl=%d)' % \
      (utc_timestamp, src_ip, src_port, dst_ip, dst_port, protocol, pkt_len, ttl)
    print (log_line)

def run():
    for ts, buf in dpkt.pcap.Reader(open(InputFile,'r')):
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        src_ip = socket.inet_ntoa(ip.src)
        src_port = str(ip.data.sport)
        dst_ip = socket.inet_ntoa(ip.dst)
        dst_port = str(ip.data.dport)
        if type(ip.data) == dpkt.tcp.TCP:
            protocol = 'tcp'
        elif type(ip.data) == dpkt.udp.UDP:    
            protocol = 'udp'
        print_packet_info(ts, src_ip, src_port, dst_ip, dst_port, protocol, ip.len, ip.ttl)

if __name__ == '__main__':
    print ""
    run()
    print ""
    pcap_summary()
