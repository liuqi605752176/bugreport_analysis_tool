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
# from matplotlib import style


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
        if mem_cache in list_line:
            mem_list.append(list_line)

    y_total = mem_list[0][1]
    y_free = mem_list[1][1]
    y_cache = mem_list[2][1]

    return y_total, y_free, y_cache


def dump_to_file(x_time, y_total, y_free, y_cache):
    dash_line = '-' * 90 + '\n'
    try:
        f = open('dump_meminfo.txt', 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = str(x_time) + ' ' + y_total + ' ' + y_free + ' ' + y_cache
    print data_line
    f.write(data_line + ' \n')
    f.close()


def setup_data_file():
    os.remove('dump_meminfo.txt')
    try:
        f = open('dump_meminfo.txt', 'a')
    except IOError:
        print 'dump meminfo file error '
        exit(1)
    data_line = '##DateTime' + ' ' + mem_total + ' ' + mem_free + ' ' + mem_cache
    print data_line
    f.write(data_line + ' \n')
    f.close()


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


def main():
    setup_data_file()
    while True:
        y_total, y_free, y_cache = get_meminfo()
        x_time = get_dev_time()
        dump_to_file(x_time, y_total, y_free, y_cache)
        time.sleep(0.5)
    sys.exit(0)


if __name__ == '__main__':
    main()
