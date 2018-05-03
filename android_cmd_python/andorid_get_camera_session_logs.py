#!/usr/bin/env python2.7

import sys
import argparse
import os
import common
import getopt

def parser(argv):
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),description='Process camera session logs')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 1.0')
    parser.add_argument('--verbose','-v',action='store_true', help='verbose loging')
    parser.add_argument('-l','--live',action='store_true', help='use live adb logcat output')
    parser.add_argument('--tags',metavar='TAG',type=str, help='parse logcat tag_names')
    parser.add_argument('--file',metavar='logcat_file.txt',nargs='?',type=check_file, help='use logcat file ')
    parser.add_argument('-c','--clear',action='store_true',help='clear adb logcat buffer')

    args = parser.parse_args(argv)
    return args


def usage():
    print " TODO: implement usage()"

def check_adb():
    print 'adb found'

def check_file(filename):
    proceed = os.path.exists(filename)
    if not proceed:
        print 'file not found : ' + filename
        sys.exit(-1)

def main():
    print sys.argv
    # # Using  argparse
    # args = parser(sys.argv[1:]);
    # print args
    try:
        opt, args = getopt.getopt(sys.argv[1:],'lcv',['help','file=','tags='])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    common.print_line()
    print "-------- opt-----------------"
    print opt
    print '----------------- args -------------'
    print args
    common.print_line()

    file = None
    verbose = None
    tags = []
    adb_live= None
    adb_clear_logs = None

    for option, arg in opt:
        if option == '-v':
            verbose = True
        elif option in ('-h','--help'):
            usage()
            sys.exit(0)
        elif option == '--file':
            file = arg
        elif option == '--tags':
            tags.append(arg.split())
        elif option == '-l':
            adb_live = True
        elif option == '-c':
            adb_clear_logs = True
        else:
            assert False, "unhandled option"


    print file
    print verbose
    print tags
    print adb_live
    print adb_clear_logs








#
# import getopt, sys
#
# def main():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
#     except getopt.GetoptError as err:
#         # print help information and exit:
#         print str(err)  # will print something like "option -a not recognized"
#         usage()
#         sys.exit(2)
#     output = None
#     verbose = False
#     for o, a in opts:
#         if o == "-v":
#             verbose = True
#         elif o in ("-h", "--help"):
#             usage()
#             sys.exit()
#         elif o in ("-o", "--output"):
#             output = a
#         else:
#             assert False, "unhandled option"
#     # ...
#
# if __name__ == "__main__":
#     main()
#









if __name__ == '__main__':
    main()
