import platform
import subprocess
import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--inputfile', help='Input FileName which contain Host Name/IP per line', required=True)
    arguments = parser.parse_args()
    InputFile = arguments.inputfile
    return InputFile
InputFile = get_args()

def OSV(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    COMM_OUT = subprocess.check_output(command, universal_newlines=True)
    if "ttl=56" in COMM_OUT:
        return "Unix"
    elif "ttl=120" in COMM_OUT:
        return "Windows"

HOSTS = open(InputFile)
for Host in HOSTS:
    OUT = OSV(Host).rstrip()
    print("{} {}".format(Host,OUT))