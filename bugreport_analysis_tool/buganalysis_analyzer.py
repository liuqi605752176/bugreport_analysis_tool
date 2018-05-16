import os
import buganalysis_utils as util
import buganalysis_filter as filter
import buganalysis_pattern as pattr
import re
WS = util.WS
'''
The buganalysis_analyzer module to analyze data and genrate report
'''
TAG = 'buganalysis_analyzer.py'

def clean_me(filename):
    if not os.path.isfile(filename):
        util.PLOGE(TAG,'file not found : ' + str(filename))
        return False
    os.remove(filename)
    return True

def start_event_log_analyzer(WS):
    '''
    # am_proc_start
    # 43 30014 am_proc_start (User|1|5),(PID|1|5),(UID|1|5),(Process Name|3),(Type|3),(Component|3)
    04-25 11:43:38.771  1000  1656  2900 I am_proc_start: [0,5092,10007,com.android.cellbroadcastreceiver,broadcast,com.android.cellbroadcastreceiver/.CellBroadcastReceiver]

    '''
    filename = filter.get_file_with_filter_data(WS.file_event_logs,pattr.am_proc_start)
    if (not filename) or not (os.path.isfile(filename)):
        util.PLOGE(TAG,'failed to set filter')
        return False

    try:
        f_buf = open(filename,'r')
    except IOError as err:
        util.PLOGE(TAG,'failed to read file : ' + str(err) )
        return False

    # get all pid list from am_proc_start
    unwanted = re.compile(r'^[[]+')
    unwanted_1 = re.compile(r'[]\n]+$')
    # list of proccess data and process log timestampdata
    list_aps_process_data = {}
    list_aps_time_data = {}

    for line_am_proc_start in f_buf:
        JP = util.JavaProcess()
        list_am_proc_start = str(line_am_proc_start).split(': ')
        list_aps_process_data = str(list_am_proc_start[1]).split(',')
        list_aps_time_data = str(list_am_proc_start[0]).split()

        for idx , item in enumerate(list_aps_process_data):
            if unwanted.search(item):
               list_aps_process_data[idx] = str(item).strip('[')
            if unwanted_1.search(item):
               list_aps_process_data[idx] = str(item).strip(']\n')

        JP.log_timestamp    = str(list_aps_time_data[0]) + '_' + str(list_aps_time_data[1])
        JP.user             = list_aps_process_data[0]
        JP.pid              = list_aps_process_data[1]
        JP.uid              = list_aps_process_data[2]
        JP.name             = list_aps_process_data[3]
        JP.p_type           = list_aps_process_data[4]
        JP.component        = list_aps_process_data[5]

        process_data_aps =  str(JP.log_timestamp) +  ' ' + \
                            str(JP.user) + ' ' + \
                            str(JP.pid) + ' ' + \
                            str(JP.uid) + ' ' + \
                            str(JP.name) + ' ' + \
                            str(JP.p_type) + ' ' + \
                            str(JP.component)
        print process_data_aps

    
    
    f_buf.close()
    clean_me(filename)





