#!/usr/bin/env python2.7

import  sys
import argparse
import subprocess
import re
import os

AVC_PATTERN = 'avc:'
DENIED_PATTERN = 'denied'
COMM_PATTERN = 'comm='
AVC_FILE = 'avc_list.txt'
AVC_LIVE_FILE = 'avc_list_live.txt'
is_adb_logcat = False

"""
Open bugreport file 

- find avc denied comm=
- 
"""

comm_list = []
split_list = []
def avc_filter(logcat_file,is_adb_logcat):
    if is_adb_logcat:
        logcat_buf = logcat_file
    else:
        logcat_buf = open(logcat_file,'rU')

    for line in logcat_buf:
        if AVC_PATTERN in line and DENIED_PATTERN in line and COMM_PATTERN in line:
            split_list= line.split()
            for word in split_list:
                if 'comm=' in word:
                    data = word.split('=')
                    if data[1] not in comm_list:
                        comm_list.append(data[1])
    if not is_adb_logcat:
        logcat_buf.close()


def avc_filter_live(logcat_file):
    if os.path.isfile(AVC_LIVE_FILE):
        os.remove(AVC_LIVE_FILE)
    f = open(AVC_LIVE_FILE,'a+')

    for line in logcat_file:
        if AVC_PATTERN in line and DENIED_PATTERN in line:
            print line,
            f.write(line)
    f.close()


def write_to_file(logcat_file,is_adb_logcat):
    # Now we have list of commands
    if os.path.isfile(AVC_FILE):
        os.remove(AVC_FILE)
    f = open(AVC_FILE,'a+')
    for cmd in comm_list:
        dash_line = '-' * 90 + '\n'
        f.write(' \n')
        f.write(cmd + ' \n')
        f.write(dash_line)

        if is_adb_logcat:
            return
        else:
            logcat_buf = open(logcat_file, 'rU')

        for line in logcat_buf:
            if AVC_PATTERN in line and DENIED_PATTERN in line and COMM_PATTERN in line:
                if cmd in line:
                    f.write(line)
        f.write(' \n')
        if not is_adb_logcat:
            logcat_buf.close()

    f.close()


def ParseArgs(argv):
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--clear", action="store_true",
                        help="clear the log buffer before running logcat")
    parser.add_argument("--logcatfile", type=str, nargs=1,
                        help="logcat file to detect avc")

    args = parser.parse_args()
    return args

def main():
    args = ParseArgs(sys.argv)

    if args.logcatfile:
        # From a file of raw logs
        try:
            infile = args.logcatfile[0]
            is_adb_logcat = False
        except IOError:
            sys.stderr.write("Error opening file for read: %s\n" % args.logcatfile[0])
            sys.exit(1)

    else:
        # From running adb logcat on an attached device
        if args.clear:
            subprocess.check_call(["adb", "logcat", "-c"])
            print 'Run test case'
        cmd = ["adb", "logcat", "-v", "long", "-D", "-v", "uid"]

        logcat = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        infile = logcat.stdout
        is_adb_logcat = True

    if is_adb_logcat:
        avc_filter_live(infile)
        sys.exit(0)

    logcat_file = infile
    avc_filter(logcat_file,is_adb_logcat)
    write_to_file(infile,is_adb_logcat)

if __name__ == '__main__':
    main()
