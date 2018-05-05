#!/usr/bin/env python2.7

import os
import subprocess
import sys
import time
import numpy as np
import matplotlib
import datetime
from time import gmtime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import localAdb as adb
import utils as util
import getopt

TAG = util.prog_name
OPT = util.OPT
mem_total = 'MemTotal:'
mem_free = 'MemFree:'
mem_ava = 'MemAvailable:'
mem_buff = 'Buffers:'
mem_cache = 'Cached:'
mem_list = []

dict_mem_type = {
    'MemTotal': None,
    'MemFree': None,
    'Cached': None
}


'''
['MemTotal:', '2803616', 'kB']
['MemFree:', '46180', 'kB']
['MemAvailable:', '632460', 'kB']
['Buffers:', '22020', 'kB']
['Cached:', '578676', 'kB']
['SwapCached:', '0', 'kB']
['Active:', '1209432', 'kB']
['Inactive:', '296652', 'kB']
['Active(anon):', '907820', 'kB']
['Inactive(anon):', '2676', 'kB']
['Active(file):', '301612', 'kB']
['Inactive(file):', '293976', 'kB']
['Unevictable:', '256', 'kB']
['Mlocked:', '256', 'kB']
['SwapTotal:', '0', 'kB']
['SwapFree:', '0', 'kB']
['Dirty:', '36', 'kB']
['Writeback:', '0', 'kB']
['AnonPages:', '905676', 'kB']
['Mapped:', '317328', 'kB']
['Shmem:', '5108', 'kB']
['Slab:', '446404', 'kB']
['SReclaimable:', '96448', 'kB']
['SUnreclaim:', '349956', 'kB']
['KernelStack:', '37456', 'kB']
['PageTables:', '49624', 'kB']
['NFS_Unstable:', '0', 'kB']
['Bounce:', '0', 'kB']
['WritebackTmp:', '0', 'kB']
['CommitLimit:', '1401808', 'kB']
['Committed_AS:', '102688840', 'kB']
['VmallocTotal:', '244318144', 'kB']
['VmallocUsed:', '200184', 'kB']
['VmallocChunk:', '243979236', 'kB']




[['MemTotal:', '2803616', 'kB'], ['MemFree:', '55996', 'kB']]







'''


def mem_filter(buf):
    mem_list = []
    for line in buf:
        list_line = line.split()
        if mem_total in list_line:
            mem_list.append(list_line)
        if mem_free in list_line:
            mem_list.append(list_line)
        if mem_ava in list_line:
            mem_list.append(list_line)
        if mem_cache in list_line:
            mem_list.append(list_line)

    y_total = mem_list[0][1]
    y_free = mem_list[1][1]
    y_ava = mem_list[2][1]
    y_cache = mem_list[3][1]

    return y_total, y_free, y_ava, y_cache


def dump_to_file(filename, x_time, y_total, y_free, y_ava, y_cache):
    try:
        f = open(filename, 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = str(x_time) + ' ' + y_total + ' ' + \
        y_free + ' ' + y_ava + ' ' + y_cache
    print data_line
    f.write(data_line + ' \n')
    f.close()


def dump_all_data_to_file(filename, x_time, y_total, y_free, y_ava, y_cache, y_ion_total):
    try:
        f = open(filename, 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = str(x_time) + ' ' + y_total + ' ' + \
        y_free + ' ' + y_ava + ' ' + y_cache + ' ' + y_ion_total
    print data_line
    f.write(data_line + ' \n')
    f.close()


def dump_ion_data_to_file(filename, x_time, y_ion_total):
    try:
        f = open(filename, 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = str(x_time) + ' ' + y_ion_total
    print data_line
    f.write(data_line + ' \n')
    f.close()


def setup_ion_data_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    try:
        f = open(filename, 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = '##DateTime' + ' ' + 'ION_Total'
    print data_line
    f.write(data_line + ' \n')
    f.close()


def setup_all_data_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    try:
        f = open(filename, 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = '##DateTime' + ' ' + mem_total + ' ' + mem_free + \
        ' ' + mem_ava + ' ' + mem_cache + ' ' + ' ION_total'
    print data_line
    f.write(data_line + ' \n')
    f.close()


def setup_data_file():
    if os.path.isfile('dump_meminfo.txt'):
        os.remove('dump_meminfo.txt')
    try:
        f = open('dump_meminfo.txt', 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = '##DateTime' + ' ' + mem_total + ' ' + mem_free + \
        ' ' + mem_ava + ' ' + mem_cache
    print data_line
    f.write(data_line + ' \n')
    f.close()


def get_ion_meminfo():
    data_list = adb.shell_command('cat /d/ion/heaps/system')
    # print data_list
    for item in data_list:
        data = str(item)
        if data.startswith('          total'):
            list_total = data.split()
            total = list_total[1].strip('\n')
            return int(total)/1024


def get_meminfo():
    mem_cmd = ['adb', 'shell', 'cat', '/proc/meminfo']
    try:
        meminfo_raw = subprocess.Popen(mem_cmd, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print 'failed to get meminfo', err
        sys.exit(-1)

    return mem_filter(meminfo_raw.stdout)


def get_dev_time():
    date_cmd = ['adb', 'shell', 'date +%d-%m-%Y_%H-%M-%S']
    # date_cmd = ['adb', 'shell', 'date +%H:%M:%S']

    try:
        dev_time = subprocess.Popen(
            date_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print 'failed to get dev time : ', err
        sys.exit(-1)

    tmp_time = dev_time.communicate()[0]
    x_time = str(tmp_time).strip('\n')
    return x_time


def plot_live_graph(x_time, y_total, y_free, y_cache):
    print x_time, y_total, y_free, y_cache
    # x_datetime = datetime.datetime.strptime(x_time, '%H:%M:%S')
    # print type(x_datetime)
    # print x_datetime
    plt.plot([datetime.datetime.now()], [int(y_cache)], 'r-')
    plt.gcf().autofmt_xdate()
    plt.ylabel('y lable')
    plt.xlabel('x lable')
    plt.draw()
    plt.pause(0.01)
    # plt.clf()


def plot_graph_animate():
    # style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):
        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)
        ax1.clear()
        ax1.plot(xs, ys)

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    plt.pause(1)


def usage():
    util.print_empty_line()
    print util.prog_name + ' ' + '<options>'
    util.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t-v,--verbose\t\t - print verbose logging'
    print '\t-m \t\t - monitor /proc/meminfo'
    print '\t-i \t\t - monitor /d/kernel/ion'
    print '\t--version\t\t - print version'
    util.print_empty_line()


def parse_argument(argv):
    long_opts = ['help', 'version', 'verbose']
    short_opts = 'hvmia'

    try:
        opts_list, args_pos = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        util.print_empty_line()
        print 'Error : args parser '
        usage()
        return False

    if args_pos:
        usage()
        return False

    for opt, val in opts_list:
        if opt in ['-h', '--help']:
            usage()
            return False
        elif opt == '--version':
            print util.get_version()
            return False
        elif opt in ['-v', '--verbose']:
            util.OPT.verbose = True
        elif opt == '-m':
            util.OPT.meminfo = True
        elif opt == '-i':
            util.OPT.ion = True
        elif opt == '-a':
            util.OPT.ionAndMeminfo = True
        else:
            print 'Error: wrong option : ' + opt
            return False

    return True


def main():
    util.prog_name = sys.argv[0]
    if not parse_argument(sys.argv):
        util.PLOGE(TAG, 'parse argument failed', exit=True)

    if not adb.is_device_online():
        print 'check adb device connection'
        sys.exit(-1)

    if OPT.meminfo:
        setup_data_file()
        while True:
            y_total, y_free, y_ava, y_cache = get_meminfo()
            x_time = get_dev_time()
            dump_to_file('dump_meminfo.txt', x_time,
                         y_total, y_free, y_ava, y_cache)
            time.sleep(0.5)
        sys.exit(0)

    if OPT.ion:
        setup_ion_data_file('dump_ion_meminfo.txt')
        while True:
            total = get_ion_meminfo()
            # y_total = get_ion_meminfo()
            x_time = get_dev_time()
            dump_ion_data_to_file('dump_ion_meminfo.txt', x_time, str(total))
            time.sleep(0.5)

    if OPT.ionAndMeminfo:
        setup_all_data_file('dump_all_meminfo.txt')
        while True:
            y_total, y_free, y_ava, y_cache = get_meminfo()
            x_time = get_dev_time()
            y_ion_total = get_ion_meminfo()

            dump_all_data_to_file('dump_all_meminfo.txt', x_time,
                                  y_total, y_free, y_ava, y_cache, str(y_ion_total))
            time.sleep(0.5)


if __name__ == '__main__':
    main()
