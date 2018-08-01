import buganalysis_utils as util
import buganalysis_pattern as pattr
import os
import re

"""system_analyzer.py class to analyze system logs
"""

TAG = os.path.basename(__file__)

def GetNativeCrashes(WS):
    """Dump native crash logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
                      str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_native_crash_buf = open(WS.file_ws_system_native_crash,'w+')
    except IOError as err:
        errorString = 'failed to create native crash log file ' + \
                      str(err)
        util.PLOGE(TAG,errorString)
        return False

    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write("--- Native crash ---")
    f_native_crash_buf.write(util.get_empty_line())
    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.start_crash_native.search(line):
            found_crash = True
            f_native_crash_buf.write(util.get_empty_line())
            f_native_crash_buf.write(util.get_line())
        if pattr.end_crash_native_conti.search(line):
            f_native_crash_buf.write(line)

    f_system_log_buf.close()
    f_native_crash_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_native_crash)
        util.PLOGV(TAG,"Opps, No native crash")

    return True

def GetAppCrashes(WS):
    """Dump application crash logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
                      str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_app_crash_buf = open(WS.file_ws_system_app_crash,'w+')
    except IOError as err:
        errorString = 'failed to create application crash log file ' + \
                      str(err)
        util.PLOGE(errorString)
        return False

    f_app_crash_buf.write(util.get_line())
    f_app_crash_buf.write("--- Application crash ---")
    f_app_crash_buf.write(util.get_empty_line())
    f_app_crash_buf.write(util.get_line())
    f_app_crash_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.start_crash_application.search(line):
            found_crash = True
            f_app_crash_buf.write(util.get_empty_line())
            f_app_crash_buf.write(util.get_line())
        if pattr.end_crash_application.search(line):
            f_app_crash_buf.write(line)


    f_system_log_buf.close()
    f_app_crash_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_app_crash)
        util.PLOGV(TAG,"Opps, No application crash")

    return True

def DumpAnrForPid(WS,pid,pid_name):
    """Dump VM TRACES for given pid and pid_name

    :param WS: Workspace object
    :param pid: pid number
    :param pid_name: process name
    :return: True on Success and False on Failure
    """
    filename = WS.dir_analysis_anr + '/' + pid + '_' + pid_name
    try:
        f_pid_anr = open(filename,'w+')
    except IOError as err:
        errorString = 'failed to create anr log file ' + \
                     filename + ' ' + str(err)
        util.PLOGE(errorString)
        return False


    patt_start = re.compile("----- pid " + pid)
    patt_end = re.compile("----- end " + pid)
    isTraceFound = False
    with open(WS.file_anr_logs,'r') as anr_logs:
        bool_start_dump = None
        for line in anr_logs:
            if bool_start_dump:
                f_pid_anr.write(line)
            if patt_start.search(line):
                f_pid_anr.write(line)
                isTraceFound = True
                bool_start_dump = True
            if patt_end.search(line):
                bool_start_dump = False
                break
        anr_logs.close()
    f_pid_anr.close()

    if not isTraceFound :
        os.remove(filename)
        return False

    return True

def GetAppAnr(WS):
    """Dump application ANR logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
    anr_pid_dict = {}
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
                      str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_app_anr_buf = open(WS.file_ws_system_anr,'w+')
    except IOError as err:
        errorString = 'failed to create application anr log file ' + \
                      str(err)
        util.PLOGE(errorString)
        return False

    f_app_anr_buf.write(util.get_line())
    f_app_anr_buf.write("--- Application ANR ---")
    f_app_anr_buf.write(util.get_empty_line())
    f_app_anr_buf.write(util.get_line())
    f_app_anr_buf.write(util.get_empty_line())
    found_crash = False

    pid_number = None
    process_name = None
    for line in f_system_log_buf:
        if pattr.start_anr_application.search(line):
            process_words = line.split(' E ')
            process_name = process_words[1].split().pop(3)
            found_crash = True
            f_app_anr_buf.write(util.get_empty_line())
            f_app_anr_buf.write(util.get_line())
        if found_crash and pattr.end_anr_application.search(line):
            if re.compile(r'ActivityManager: PID:').search(line):
                word_list = line.split();
                pid_number = word_list[len(word_list) - 1]
                anr_pid_dict[pid_number] = process_name
                pid_number = None
                process_name = None
            f_app_anr_buf.write(line)

    f_system_log_buf.close()
    f_app_anr_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_anr)
        util.PLOGV(TAG,"Opps, No application ANR")

    for pid,pid_name in anr_pid_dict.iteritems():
        if (pid and pid_name) is None:
            continue

        if not DumpAnrForPid(WS,pid,pid_name):
            util.PLOGE(TAG,"Failed to get or not found ANR traces for : " + \
                       str(pid) + ' - ' + str(pid_name))

    return True



def DumpPowerLogs(WS):
    """Dump power logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
    try:
        f_power_logs_buf = open(WS.file_power_logs, 'a+')
    except IOError as err:
        error = 'failed to create power log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

    try:
        f_sys_logs_buf = open(WS.file_system_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

    try:
        f_kernel_logs_buf = open(WS.file_kernel_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

    f_power_logs_buf.write('--- PowerManager ---')
    f_power_logs_buf.write(util.get_empty_line())
    f_power_logs_buf.write(util.get_empty_line())

    for line in f_sys_logs_buf:
        if pattr.device_sys_sleep_power_button.search(line) or \
                pattr.device_sys_sleep_screen_timeout.search(line) or \
                pattr.device_sys_wake_up.search(line):
            f_power_logs_buf.write(line)
    f_power_logs_buf.write(util.get_empty_line())

    f_power_logs_buf.write('--- Kernel ---')
    f_power_logs_buf.write(util.get_empty_line())
    f_power_logs_buf.write(util.get_empty_line())


    for line in f_kernel_logs_buf:
        if pattr.device_kernel_sleep.search(line) or \
                pattr.device_sys_sleep_screen_timeout.search(line) or \
                pattr.device_kernel_wakeup.search(line):
            f_power_logs_buf.write(line)
    f_power_logs_buf.write(util.get_empty_line())

    f_power_logs_buf.close()
    f_sys_logs_buf.close()
    f_kernel_logs_buf.close()
    return True

