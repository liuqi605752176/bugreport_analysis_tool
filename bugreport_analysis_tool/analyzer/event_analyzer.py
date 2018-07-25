import buganalysis_utils as util
import filter
import buganalysis_pattern as pattr
import os
import re
from analyzer import event_classes as evntClasses

""" event_analyzer.py module to analyze only event logs
"""
TAG = os.path.basename(__file__)

def IsLineContainPid(pid,line):
    """Check pid number exists in event log line

    :param pid: process id to be check in line
    :param line: log line
    :return: True on success and Flase on failure
    """
    pattern_pid  = re.compile(',' + pid)
    pattern_pid1 = re.compile(r'[ ]' + pid)
    pattern_pid2 = re.compile(pid + ',')
    st = pattern_pid.search(line)
    st1 = pattern_pid1.search(line)
    st2 = pattern_pid2.search(line)

    if not (st or st1 or st2 ):
        return False

    return True

def GetEventTag(tag,line):
    """Read line and fill tag data

    :param tag: Tag class object
    :param line: line to be filter
    :return: True on success and False on Failure
    """
    if not line:
        return False
    list_raw_words = str(line).split(': ')
    list_words = list_raw_words[0].split()
    tag.date = list_words[0]
    tag.time = list_words[1]
    tag.log_uid = list_words[2]
    tag.log_pid = list_words[3]
    tag.log_tid = list_words[4]
    tag.log_level = list_words[5]
    tag.tag_name = list_words[6]
    return True

def FilterByPid(WS):
    """ Filter event logs by PID from am_start_proc filter

    :param WS: WorkSpace object
    :return:True on success and False on Failure
    """
    tmpfile = filter.GetFileWithFilterData(WS.file_event_logs,pattr.am_proc_start)
    if (not tmpfile) or not (os.path.isfile(tmpfile)):
        util.PLOGE(TAG,'failed to set filter')
        return False

    try:
        f_buf = open(tmpfile,'r')
    except IOError as err:
        util.PLOGE(TAG,'failed to read file : ' + str(err) )
        return False

    try:
        f_event_aps_buf  = open(WS.file_ws_events_am_proc_start,'w+')
    except IOError as err:
        util.PLOGE(TAG,'failed to read file : ' + str(err) )
        return False

    process_data_aps_title = '##log_timestamp user pid uid name p_typ component data_aps'
    f_event_aps_buf.write(process_data_aps_title)
    f_event_aps_buf.write(util.get_empty_line())

    # get all pid list from am_proc_start
    unwanted = re.compile(r'^[[]+')
    unwanted_1 = re.compile(r'[]\n]+$')
    list_jp_pid = []

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
                            ' '* (6 - len(JP.uid)) + \
                            str(JP.name) + ' ' + \
                            ' '* (50 - len(JP.name)) + \
                            str(JP.p_type) + ' ' + \
                            ' '* (20 - len(JP.p_type)) + \
                            str(JP.component)
        # print process_data_aps
        f_event_aps_buf.write(process_data_aps)
        f_event_aps_buf.write(util.get_empty_line())

        set_warning = None
        if not JP.pid in list_jp_pid:
            list_jp_pid.append(JP.pid)
        else:
            util.PLOGV(TAG,"The duplicate pid found : " + str(JP.pid))
            set_warning = True
            list_jp_pid.append(JP.pid)

        pid_dir_name = WS.dir_ws_analysis_bypid + '/' + JP.pid
        file_jp_pid_events =  pid_dir_name + '/' + 'events_' + JP.pid +'.txt'

        if not os.path.exists(pid_dir_name):
            os.makedirs(pid_dir_name)

        #Open main events file and check for current JP.pid
        util.PLOGV(TAG," dump event data for : " + pid_dir_name)
        try:
            f_event_buf = open(WS.file_event_logs,'rU')
        except IOError as err:
            error_str = 'failed to read event file for pid : ' + \
                        JP.pid  + '\n' + str(err)
            util.PLOGE(TAG,error_str)
            return False

        try:
            f_jp_pid_events = open(file_jp_pid_events,'a+')
        except IOError as err:
            error_str = 'failed to create file_jp_pid_events file for pid : ' + \
                        JP.pid  + '\n' + str(err)
            util.PLOGE(TAG,error_str)
            return False
        if set_warning:
            msg_warn_L1 = "Warning *********************************************************** \n"
            msg_warn_L2 = "Warning ** The " +  JP.pid + " might be dumplicate please check *** \n"
            msg_warn_L3 = "Warning *********************************************************** \n"
            util.PLOGV(TAG,msg_warn_L1)
            util.PLOGV(TAG,msg_warn_L2)
            util.PLOGV(TAG,msg_warn_L3)

            f_jp_pid_events.write(msg_warn_L1 + msg_warn_L2 + msg_warn_L3)
            set_warning = None
            msg_warn_L1 = None
            msg_warn_L2 = None
            msg_warn_L3 = None

        #skip title lines
        for each in [1,2,3]:
            f_event_buf.readline()

        for event_line in f_event_buf:
            if pattr.end_event_log.search(event_line):
                break
            mTag = evntClasses.Tag()
            if not GetEventTag(mTag,event_line):
                continue
            if not IsLineContainPid(JP.pid,event_line):
                continue
            f_jp_pid_events.write(event_line)
        f_event_buf.close()

    f_buf.close()
    f_event_aps_buf.close()
    util.clean_me(tmpfile)


def DumpScreenOnOffLogs(WS):
    """ Dump screen on and off logs i.e display on off

    :param WS: Workspace object
    :return: True on sccess and False on failure
    """
    try:
        f_power_logs_buf = open(WS.file_power_logs,'w+')
    except IOError as err:
        error = 'failed to create power log file : ' + str(err)
        util.PLOGE(TAG,error)

    try:
        f_event_logs_buf = open(WS.file_event_logs,'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)

    util.PrintLogFileTitle(f_power_logs_buf,'Power logs')
    f_power_logs_buf.write('--- Screen ON and OFF ---')
    f_power_logs_buf.write(util.get_empty_line())
    f_power_logs_buf.write(util.get_empty_line())


    for line in f_event_logs_buf:
        if pattr.screen_on.search(line) or \
                pattr.screen_off.search(line) :
            f_power_logs_buf.write(line)
    f_power_logs_buf.write(util.get_empty_line())

    f_power_logs_buf.close()
    f_event_logs_buf.close()


def StartAnalyzer(WS):
    """Event log analyzer func

    :param WS: WrokSpace class object1
    :return: None
    """
    filter.FilterByTagInFilesList(WS)
    FilterByPid(WS)
    DumpScreenOnOffLogs(WS)






