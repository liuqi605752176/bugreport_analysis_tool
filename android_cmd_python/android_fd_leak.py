import localAdb as adb
import os
import time
import sys
import android_utils as util
import getopt as getopt
import shutil

TAG  = "android_fd_leak"
debug_mode = False

class ProcessInfo(object):
    def __init__(self):
        self.name = None
        self.pid = None

def dumpdata(PROCESS,data,file):
    try:
        f_data = open(file,'a+')
    except IOError as err:
        err_string = 'failed to create : ' + file + '  ERORR : ' + str(err)
        util.PLOGE(TAG,err_string)
        return False
    f_data.write(data)
    f_data.close()


def monitorFdLeakFor(PROCESS):
    pid = PROCESS.pid
    cmd  =  'lsof -p ' + pid
    if util.OPT.out is None:
        util.PLOGE(TAG,"out dir location missed ")
        usage()
        return False

    if os.path.exists(util.OPT.out):
        shutil.rmtree(util.OPT.out)

    os.mkdir(util.OPT.out)

    file_data = util.OPT.out + '/' + 'fd_leak.txt'
    util.PLOGE(TAG," Data File : " + file_data)
    title_str = '#dateTime pid fdcount' + '\n'
    dumpdata(PROCESS,title_str,file_data)

    while True:
        time.sleep(0.5)
        data = adb.shell_command(cmd)
        fdcount = len(data)
        datetime = adb.shell_command('date +%d-%m-%Y_%H-%M-%S')
        datetime = str(datetime[0]).strip('\n')
        if not type(data) == list:
            util.PLOGE(TAG,"failed  to get data")
            return False

        data_string = datetime + ' ' + str(fdcount) + '\n'
        util.PLOGV(TAG,data_string,strip=True)
        dumpdata(PROCESS,data_string,file_data)
        # f_data.close()

        data = None

def getSystemSeverpid(PROCESS):
    data = adb.shell_command('ps -ef |grep system_server')
    data_list = str(data[0]).split()
    PROCESS.name = data_list[0]
    PROCESS.pid = data_list[1]

def usage():
    util.print_empty_line()
    util.print_line()
    print util.prog_name + ' ' + '<options> ' + ' --pid ' + ' <pid> '
    util.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t--out <out_dir>\t\t - output dir'
    print '\t--pid\t\t - Give pid to monitor fd leak'
    util.print_empty_line()

def parse_argument(argv):
    long_opts = ['help', 'verbose','out=', 'pid=']
    short_opts = 'hv'

    try:
        opts_list, args_pos = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        util.print_empty_line()
        print 'Error : args parser '
        usage()
        return False

    if debug_mode:
        util.OPT.debug = True

    util.PLOGD(TAG, 'opts are :', str(opts_list))
    util.PLOGD(TAG, 'args are :', str(args_pos))

    opt_pid_found = False

    for list_child in opts_list:
        if '--pid' in list_child:
            opt_pid_found = True

    if not opt_pid_found:
        util.PLOGE(TAG,' pid not given ')
        usage()
        return False

    if args_pos:
        usage()
        return False

    for opt, val in opts_list:
        if opt == '--out':
            util.OPT.out = val
        elif opt in ['-h', '--help']:
            usage()
            return False
        elif opt == '--pid':
            util.OPT.pid = val
            print val
        elif opt in ['-v', '--verbose']:
            util.OPT.verbose = True
            print "verbose logging"
        else:
            print 'Error: wrong option : ' + opt
            return False

    return True

def main():
    util.prog_name = sys.argv[0]
    TAG = util.prog_name

    # if not sys.argv[1]:
    #      usage()
    #      sys.exit(-1)

    if not parse_argument(sys.argv):
        util.PLOGE(TAG, 'parse argument failed', exit=True)

    PROCESS = ProcessInfo()
    adb.wait_for_adb()
    getSystemSeverpid(PROCESS)
    monitorFdLeakFor(PROCESS)

if __name__ == '__main__':
    main()